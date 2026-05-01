import os
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)

# ============================================================
# User settings
# ============================================================

N_THREADS = 4
ROOT.EnableImplicitMT(N_THREADS)

INPUT_FILE  = "Ntuple_AnaQCDFlat_NanoV15_MC24_QCD_Flat2022_LO_py8.root"
INPUT_TREE  = "Events"
OUTPUT_FILE = "scripts/JetResponse_Fig10.root"

ADD_PROGRESS_BAR = True

# ------------------------------------------------------------
# Event cleaning
# For pure MC response studies this can stay False.
# Set True if you want to apply NanoAOD event-quality flags.
# ------------------------------------------------------------
USE_EVENT_CLEANING = False

EVENT_CLEANING_FILTER = (
    "Flag_goodVertices && "
    "Flag_globalSuperTightHalo2016Filter && "
    "Flag_EcalDeadCellTriggerPrimitiveFilter && "
    "Flag_BadPFMuonFilter && "
    "Flag_BadPFMuonDzFilter && "
    "Flag_hfNoisyHitsFilter && "
    "Flag_eeBadScFilter && "
    "Flag_ecalBadCalibFilter"
)

# ------------------------------------------------------------
# Matching / acceptance
# ------------------------------------------------------------
JET_ETA_MAX = 5.2
MATCH_DR_MAX = 0.25  # R/2 for R = 0.5

# ------------------------------------------------------------
# Figure 10(a)
# Response vs |eta_reco| in fixed pT_ptcl windows
#
# FIG10A_RECO_PT_MODE:
#   "raw"  -> use Jet_pt * (1 - Jet_rawFactor)
#   "corr" -> use Jet_pt
#
# CMS Fig. 10(a) is conceptually after pileup handling.
# With this ntuple, exact pileup-offset correction cannot be
# reconstructed because rho and Jet_area are not available.
# ------------------------------------------------------------
FIG10A_RECO_PT_MODE = "raw"

PT_WINDOWS_A = {
    "10":   (9.0,    11.0),
    "30":   (28.0,   32.0),
    "100":  (90.0,  110.0),
    "400":  (380.0, 420.0),
    "2000": (1900.0, 2100.0),
}

ETA_BINS_A = (48, 0.0, 4.8)

# ------------------------------------------------------------
# Figure 10(b)
# Response after JEC vs pT_ptcl in eta regions
# ------------------------------------------------------------
ETA_REGIONS_B = {
    "BB":  (0.0, 1.3),
    "EC1": (1.3, 2.5),
    "EC2": (2.5, 3.0),
    "HF":  (3.0, 4.5),
}
#Old binning:
#PT_BINS_B = array("f", [20, 30, 50, 80, 120, 200, 400, 800, 2000])

# New binning with more points in low pT:
PT_BINS_B = array("f", [
    20, 25, 30, 40, 50, 65, 80, 100, 120,
    160, 200, 300, 400, 600, 800, 1200, 1600, 2000
])


# ============================================================
# Basic input checks
# ============================================================

if FIG10A_RECO_PT_MODE not in {"raw", "corr"}:
    raise ValueError("FIG10A_RECO_PT_MODE must be either 'raw' or 'corr'.")

input_file_check = ROOT.TFile.Open(INPUT_FILE)
if not input_file_check or input_file_check.IsZombie():
    raise OSError(f"Could not open input file: {INPUT_FILE}")

tree_check = input_file_check.Get(INPUT_TREE)
if not tree_check:
    raise KeyError(f"Could not find tree '{INPUT_TREE}' in file '{INPUT_FILE}'")

required_branches = [
    "nJet",
    "Jet_pt",
    "Jet_eta",
    "Jet_phi",
    "Jet_rawFactor",
    "Jet_genJetIdx",
    "nGenJet",
    "GenJet_pt",
    "GenJet_eta",
    "GenJet_phi",
]

if USE_EVENT_CLEANING:
    required_branches += [
        "Flag_goodVertices",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_BadPFMuonFilter",
        "Flag_BadPFMuonDzFilter",
        "Flag_hfNoisyHitsFilter",
        "Flag_eeBadScFilter",
        "Flag_ecalBadCalibFilter",
    ]

missing = [br for br in required_branches if not tree_check.GetBranch(br)]
input_file_check.Close()

if missing:
    raise RuntimeError(
        "Missing required branches:\n  " + "\n  ".join(missing)
    )

# ============================================================
# C++ helpers
# ============================================================

ROOT.gInterpreter.Declare(f"""
#include <cmath>
#include "ROOT/RVec.hxx"

using ROOT::VecOps::RVec;

// ------------------------------------------------------------
// Basic angle helpers
// ------------------------------------------------------------
float DeltaPhi(float phi1, float phi2)
{{
    float dphi = phi1 - phi2;
    while (dphi >  M_PI) dphi -= 2.f*M_PI;
    while (dphi <= -M_PI) dphi += 2.f*M_PI;
    return dphi;
}}

float DeltaR(float eta1, float phi1, float eta2, float phi2)
{{
    const float deta = eta1 - eta2;
    const float dphi = DeltaPhi(phi1, phi2);
    return std::sqrt(deta*deta + dphi*dphi);
}}

// ------------------------------------------------------------
// Figure 10 matching mask
//   - valid gen index
//   - |eta_reco| < {JET_ETA_MAX}
//   - DeltaR(reco, gen) < {MATCH_DR_MAX}
// ------------------------------------------------------------
RVec<char> BuildMatchedJetMaskFig10(const RVec<short>& jet_gen_idx,
                                    const RVec<float>& jet_eta,
                                    const RVec<float>& jet_phi,
                                    const RVec<float>& genjet_eta,
                                    const RVec<float>& genjet_phi,
                                    int nGenJet)
{{
    const size_t n = jet_eta.size();
    RVec<char> mask(n, 0);

    for (size_t i = 0; i < n; ++i) {{
        const int igen = jet_gen_idx[i];

        if (igen < 0) continue;
        if (igen >= nGenJet) continue;
        if (std::abs(jet_eta[i]) >= {JET_ETA_MAX}f) continue;

        const float dr = DeltaR(jet_eta[i], jet_phi[i],
                                genjet_eta[igen], genjet_phi[igen]);

        if (dr >= {MATCH_DR_MAX}f) continue;

        mask[i] = 1;
    }}

    return mask;
}}

// ------------------------------------------------------------
// Apply mask to RVec<float>
// ------------------------------------------------------------
RVec<float> ApplyMaskFloat(const RVec<float>& v, const RVec<char>& mask)
{{
    RVec<float> out;
    out.reserve(v.size());

    for (size_t i = 0; i < v.size(); ++i) {{
        if (mask[i]) out.push_back(v[i]);
    }}

    return out;
}}

// ------------------------------------------------------------
// Take matched gen values using reco -> gen index
// ------------------------------------------------------------
RVec<float> TakeMatchedGenFloat(const RVec<float>& gen_values,
                                const RVec<short>& jet_gen_idx,
                                const RVec<char>& mask)
{{
    RVec<float> out;
    out.reserve(jet_gen_idx.size());

    for (size_t i = 0; i < jet_gen_idx.size(); ++i) {{
        if (!mask[i]) continue;
        out.push_back(gen_values[jet_gen_idx[i]]);
    }}

    return out;
}}

// ------------------------------------------------------------
// Raw pT from corrected pT and NanoAOD rawFactor
// ------------------------------------------------------------
RVec<float> RawPt(const RVec<float>& jet_pt,
                  const RVec<float>& jet_rawFactor)
{{
    RVec<float> out;
    out.reserve(jet_pt.size());

    for (size_t i = 0; i < jet_pt.size(); ++i) {{
        out.push_back(jet_pt[i] * (1.f - jet_rawFactor[i]));
    }}

    return out;
}}

// ------------------------------------------------------------
// Absolute value of vector
// ------------------------------------------------------------
RVec<float> AbsVec(const RVec<float>& v)
{{
    RVec<float> out;
    out.reserve(v.size());

    for (auto x : v) {{
        out.push_back(std::abs(x));
    }}

    return out;
}}

// ------------------------------------------------------------
// pT window in particle-level pT
// ------------------------------------------------------------
RVec<char> PtWindowMask(const RVec<float>& pt, float low, float high)
{{
    RVec<char> mask(pt.size(), 0);

    for (size_t i = 0; i < pt.size(); ++i) {{
        if (pt[i] >= low && pt[i] < high) mask[i] = 1;
    }}

    return mask;
}}

// ------------------------------------------------------------
// eta-region mask
// ------------------------------------------------------------
RVec<char> EtaRegionMask(const RVec<float>& abs_eta, float low, float high)
{{
    RVec<char> mask(abs_eta.size(), 0);

    for (size_t i = 0; i < abs_eta.size(); ++i) {{
        if (abs_eta[i] >= low && abs_eta[i] < high) mask[i] = 1;
    }}

    return mask;
}}
""")

# ============================================================
# RDataFrame setup
# ============================================================

df = ROOT.RDataFrame(INPUT_TREE, INPUT_FILE)

if ADD_PROGRESS_BAR:
    ROOT.RDF.Experimental.AddProgressBar(df)

# Light prefilter: events must contain reco and gen jets
df = df.Filter("nJet > 0 && nGenJet > 0", "has reco and gen jets")

if USE_EVENT_CLEANING:
    df = df.Filter(EVENT_CLEANING_FILTER, "event cleaning flags")

# ============================================================
# Matched reco/gen jet construction
# ============================================================

df = df.Define(
    "jet_mask",
    "BuildMatchedJetMaskFig10("
    "Jet_genJetIdx, Jet_eta, Jet_phi, GenJet_eta, GenJet_phi, nGenJet)"
)

df = df.Define("Jet_rawPt_all", "RawPt(Jet_pt, Jet_rawFactor)")

# Selected reconstructed jets
df = df.Define("sel_reco_pt",  "ApplyMaskFloat(Jet_pt,       jet_mask)")
df = df.Define("sel_raw_pt",   "ApplyMaskFloat(Jet_rawPt_all, jet_mask)")
df = df.Define("sel_reco_eta", "ApplyMaskFloat(Jet_eta,      jet_mask)")
df = df.Define("sel_reco_phi", "ApplyMaskFloat(Jet_phi,      jet_mask)")

# Selected matched particle-level jets
df = df.Define(
    "sel_gen_pt",
    "TakeMatchedGenFloat(GenJet_pt, Jet_genJetIdx, jet_mask)"
)

df = df.Define(
    "sel_gen_eta",
    "TakeMatchedGenFloat(GenJet_eta, Jet_genJetIdx, jet_mask)"
)

df = df.Define(
    "sel_gen_phi",
    "TakeMatchedGenFloat(GenJet_phi, Jet_genJetIdx, jet_mask)"
)

# Common variables
df = df.Define("sel_abs_eta", "AbsVec(sel_reco_eta)")
df = df.Define("nSelJet", "int(sel_reco_pt.size())")
df = df.Filter("nSelJet > 0", "at least one selected matched jet")

# Choose numerator pT for Fig. 10(a)
if FIG10A_RECO_PT_MODE == "raw":
    df = df.Define("sel_fig10a_reco_pt", "sel_raw_pt")
elif FIG10A_RECO_PT_MODE == "corr":
    df = df.Define("sel_fig10a_reco_pt", "sel_reco_pt")

# ============================================================
# Helper functions for histogram creation
# ============================================================

def book_ratio_inputs_vs_eta(df, label, pt_low, pt_high):
    """
    Book numerator and denominator histograms for Fig. 10(a).

    Response:
        R_ptcl([pT_ptcl, eta_reco])
        = sum(pT_reco) / sum(pT_ptcl)
    """
    mask_name = f"mask_pt{label}"
    eta_name  = f"eta_pt{label}"
    reco_name = f"reco_ptA_{label}"
    gen_name  = f"genPt_pt{label}"

    df = df.Define(mask_name, f"PtWindowMask(sel_gen_pt, {pt_low}f, {pt_high}f)")
    df = df.Define(eta_name,  f"ApplyMaskFloat(sel_abs_eta,        {mask_name})")
    df = df.Define(reco_name, f"ApplyMaskFloat(sel_fig10a_reco_pt, {mask_name})")
    df = df.Define(gen_name,  f"ApplyMaskFloat(sel_gen_pt,         {mask_name})")

    h_reco = df.Histo1D(
        (f"h_reco_sum_eta_{label}", "", *ETA_BINS_A),
        eta_name,
        reco_name,
    )

    h_gen = df.Histo1D(
        (f"h_gen_sum_eta_{label}", "", *ETA_BINS_A),
        eta_name,
        gen_name,
    )

    return df, h_reco, h_gen


def book_ratio_inputs_vs_pt(df, region, eta_low, eta_high):
    """
    Book numerator and denominator histograms for Fig. 10(b).

    Response after JEC:
        R_ptcl([pT_ptcl, eta_reco])
        = sum(pT_reco_corrected) / sum(pT_ptcl)

    Also books raw pT numerator for comparison.
    """
    mask_name = f"mask_{region}"
    gen_name  = f"genPt_{region}"
    reco_name = f"recoPt_{region}"
    raw_name  = f"rawPt_{region}"

    df = df.Define(mask_name, f"EtaRegionMask(sel_abs_eta, {eta_low}f, {eta_high}f)")
    df = df.Define(gen_name,  f"ApplyMaskFloat(sel_gen_pt,  {mask_name})")
    df = df.Define(reco_name, f"ApplyMaskFloat(sel_reco_pt, {mask_name})")
    df = df.Define(raw_name,  f"ApplyMaskFloat(sel_raw_pt,  {mask_name})")

    h_reco = df.Histo1D(
        (f"h_reco_{region}", "", len(PT_BINS_B)-1, PT_BINS_B),
        gen_name,
        reco_name,
    )

    h_raw = df.Histo1D(
        (f"h_raw_{region}", "", len(PT_BINS_B)-1, PT_BINS_B),
        gen_name,
        raw_name,
    )

    h_gen = df.Histo1D(
        (f"h_gen_{region}", "", len(PT_BINS_B)-1, PT_BINS_B),
        gen_name,
        gen_name,
    )

    return df, h_reco, h_raw, h_gen


def make_ratio_hist(hnum, hden, name, title):
    """
    Clone numerator histogram and divide by denominator histogram.
    """
    h = hnum.Clone(name)
    h.SetTitle(title)
    h.Divide(hden)
    return h


# ============================================================
# Book Figure 10(a) histograms
# ============================================================

fig10a_reco_hists = {}
fig10a_gen_hists = {}

for label, (pt_low, pt_high) in PT_WINDOWS_A.items():
    df, h_reco, h_gen = book_ratio_inputs_vs_eta(df, label, pt_low, pt_high)
    fig10a_reco_hists[label] = h_reco
    fig10a_gen_hists[label] = h_gen

# ============================================================
# Book Figure 10(b) histograms
# ============================================================

fig10b_reco_hists = {}
fig10b_raw_hists = {}
fig10b_gen_hists = {}

for region, (eta_low, eta_high) in ETA_REGIONS_B.items():
    df, h_reco, h_raw, h_gen = book_ratio_inputs_vs_pt(df, region, eta_low, eta_high)
    fig10b_reco_hists[region] = h_reco
    fig10b_raw_hists[region] = h_raw
    fig10b_gen_hists[region] = h_gen

# ============================================================
# Trigger event loop and build response histograms
# ============================================================

fig10a_response_hists = {}
fig10a_reco_values = {}
fig10a_gen_values = {}

for label in PT_WINDOWS_A:
    h_reco = fig10a_reco_hists[label].GetValue()
    h_gen  = fig10a_gen_hists[label].GetValue()

    fig10a_reco_values[label] = h_reco
    fig10a_gen_values[label] = h_gen

    fig10a_response_hists[label] = make_ratio_hist(
        h_reco,
        h_gen,
        f"h_resp_eta_{label}",
        f"{label} GeV",
    )

fig10b_response_hists = {}
fig10b_raw_response_hists = {}
fig10b_reco_values = {}
fig10b_raw_values = {}
fig10b_gen_values = {}

for region in ETA_REGIONS_B:
    h_reco = fig10b_reco_hists[region].GetValue()
    h_raw  = fig10b_raw_hists[region].GetValue()
    h_gen  = fig10b_gen_hists[region].GetValue()

    fig10b_reco_values[region] = h_reco
    fig10b_raw_values[region] = h_raw
    fig10b_gen_values[region] = h_gen

    fig10b_response_hists[region] = make_ratio_hist(
        h_reco,
        h_gen,
        f"h_resp_pt_{region}",
        region,
    )

    fig10b_raw_response_hists[region] = make_ratio_hist(
        h_raw,
        h_gen,
        f"h_resp_raw_pt_{region}",
        f"{region} (raw)",
    )

# ============================================================
# Save output
# ============================================================

output_dir = os.path.dirname(OUTPUT_FILE)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

outFile = ROOT.TFile(OUTPUT_FILE, "RECREATE")

# Metadata
ROOT.TNamed("INPUT_FILE", INPUT_FILE).Write()
ROOT.TNamed("INPUT_TREE", INPUT_TREE).Write()
ROOT.TNamed("FIG10A_RECO_PT_MODE", FIG10A_RECO_PT_MODE).Write()
ROOT.TNamed("MATCH_DR_MAX", str(MATCH_DR_MAX)).Write()
ROOT.TNamed("JET_ETA_MAX", str(JET_ETA_MAX)).Write()
ROOT.TNamed("USE_EVENT_CLEANING", str(USE_EVENT_CLEANING)).Write()

# Figure 10(a): intermediates and final response
for label in PT_WINDOWS_A:
    fig10a_reco_values[label].Write()
    fig10a_gen_values[label].Write()
    fig10a_response_hists[label].Write()

# Figure 10(b): intermediates and final response
for region in ETA_REGIONS_B:
    fig10b_reco_values[region].Write()
    fig10b_raw_values[region].Write()
    fig10b_gen_values[region].Write()
    fig10b_response_hists[region].Write()
    fig10b_raw_response_hists[region].Write()

outFile.Close()

print("=" * 70)
print("Done.")
print(f"Output file          : {OUTPUT_FILE}")
print(f"Input file           : {INPUT_FILE}")
print(f"Figure 10(a) pT mode : {FIG10A_RECO_PT_MODE}")
print(f"Event cleaning       : {USE_EVENT_CLEANING}")
print(f"Matching dR max      : {MATCH_DR_MAX}")
print(f"Jet |eta| max        : {JET_ETA_MAX}")
print("=" * 70)

if FIG10A_RECO_PT_MODE == "raw":
    print(
        "NOTE: Figure 10(a) uses raw pT from Jet_pt * (1 - Jet_rawFactor). "
        "This does not reproduce the CMS pileup-offset-corrected stage exactly."
    )
