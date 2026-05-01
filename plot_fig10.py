import os
import math
import ROOT

ROOT.gROOT.SetBatch(True)

# ============================================================
# Configuration / tweakables
# ============================================================

# ------------------------------------------------------------
# Input / output
# ------------------------------------------------------------
INPUT_FILE = "scripts/JetResponse_Fig10.root"
#INPUT_FILE = "scripts/JetResponse_Fig10_corrected.root"


OUTPUT_FIG10A_PDF = "plots/Figure10a.pdf"
OUTPUT_FIG10A_PNG = "plots/Figure10a.png"

OUTPUT_FIG10B_PDF = "plots/Figure10b.pdf"
OUTPUT_FIG10B_PNG = "plots/Figure10b.png"

OUTPUT_FIG10B_RAW_PDF = "plots/Figure10b_raw.pdf"
OUTPUT_FIG10B_RAW_PNG = "plots/Figure10b_raw.png"

# ------------------------------------------------------------
# Canvas settings
# ------------------------------------------------------------
CANVAS_WIDTH  = 900
CANVAS_HEIGHT = 700

LEFT_MARGIN   = 0.12
RIGHT_MARGIN  = 0.04
BOTTOM_MARGIN = 0.12
TOP_MARGIN    = 0.08

# ------------------------------------------------------------
# Header settings
# ------------------------------------------------------------
HEADER_X      = 0.14
SUBHEADER_X   = 0.30
HEADER_Y      = 0.93

SHOW_METADATA_IN_FIG10A_HEADER = True
SHOW_METADATA_IN_FIG10B_HEADER = True

# ------------------------------------------------------------
# Figure 10(a) strings
# ------------------------------------------------------------
TITLE_FIG10A      = ""
XLABEL_FIG10A     = "|#eta_{reco}|"
YLABEL_FIG10A     = "R_{ptcl} = #LTp_{T}#GT / #LTp_{T,ptcl}#GT"
HEADER_FIG10A     = "CMS"
SUBHEADER_FIG10A_BASE = "anti-k_{T}, R = 0.5, #DeltaR < 0.25"

LEGEND_LABEL_10   = "p_{T,ptcl} = 10 GeV"
LEGEND_LABEL_30   = "p_{T,ptcl} = 30 GeV"
LEGEND_LABEL_100  = "p_{T,ptcl} = 100 GeV"
LEGEND_LABEL_400  = "p_{T,ptcl} = 400 GeV"
LEGEND_LABEL_2000 = "p_{T,ptcl} = 2000 GeV"

# Histogram names in the ROOT file
HIST_FIG10A = {
    LEGEND_LABEL_10:   "h_resp_eta_10",
    LEGEND_LABEL_30:   "h_resp_eta_30",
    LEGEND_LABEL_100:  "h_resp_eta_100",
    LEGEND_LABEL_400:  "h_resp_eta_400",
    LEGEND_LABEL_2000: "h_resp_eta_2000",
}

# Axis range for Figure 10(a)
XMIN_FIG10A = 0.0
XMAX_FIG10A = 4.8
YMIN_FIG10A = 0.50
YMAX_FIG10A = 1.25

# ------------------------------------------------------------
# Figure 10(a): eta-region markings
# ------------------------------------------------------------
DRAW_ETA_REGION_LINES   = True
DRAW_ETA_REGION_LABELS  = True

ETA_BOUNDARY_BB_EC1  = 1.3
ETA_BOUNDARY_EC1_EC2 = 2.5
ETA_BOUNDARY_EC2_HF  = 3.0
ETA_BOUNDARY_HF_END  = 4.5

ETA_REGION_LINE_COLOR = ROOT.kGray + 1
ETA_REGION_LINE_STYLE = 3
ETA_REGION_LINE_WIDTH = 2

# Label positions in user coordinates
ETA_LABEL_Y = 1.04

ETA_LABEL_BB_X  = 0.45
ETA_LABEL_EC1_X = 1.90
ETA_LABEL_EC2_X = 2.60
ETA_LABEL_HF_X  = 3.75

ETA_LABEL_BB  = "Barrel BB"
ETA_LABEL_EC1 = "EC1"
ETA_LABEL_EC2 = "EC2"
ETA_LABEL_HF  = "HF"

# ------------------------------------------------------------
# Per-curve visible x-ranges for Figure 10(a)
# Each curve is drawn only in this eta range.
# ------------------------------------------------------------
USE_PER_CURVE_ETA_LIMITS = True

ETA_RANGE_BY_CURVE = {
    LEGEND_LABEL_10:   (0.0, 4.8),
    LEGEND_LABEL_30:   (0.0, 4.8),
    LEGEND_LABEL_100:  (0.0, 4.4),
    LEGEND_LABEL_400:  (0.0, 3.0),
    LEGEND_LABEL_2000: (0.0, 1.3),
}

# Legend box for Figure 10(a)
LEG1_X1 = 0.14
LEG1_Y1 = 0.15
LEG1_X2 = 0.42
LEG1_Y2 = 0.42

# Reference line for Figure 10(a)
REFLINE_FIG10A_Y = 1.0

# ------------------------------------------------------------
# Figure 10(b) strings
# ------------------------------------------------------------
TITLE_FIG10B      = ""
XLABEL_FIG10B     = "p_{T,ptcl} [GeV]"
YLABEL_FIG10B     = "R_{ptcl} = #LTp_{T}#GT / #LTp_{T,ptcl}#GT"
HEADER_FIG10B     = "CMS"
SUBHEADER_FIG10B_BASE = "Simulated particle response after JEC"

LEGEND_LABEL_BB   = "BB  |#eta| < 1.3"
LEGEND_LABEL_EC1  = "EC1 1.3 < |#eta| < 2.5"
LEGEND_LABEL_EC2  = "EC2 2.5 < |#eta| < 3.0"
LEGEND_LABEL_HF   = "HF  3.0 < |#eta| < 4.5"

# Histogram names in the ROOT file
HIST_FIG10B = {
    LEGEND_LABEL_BB:  "h_resp_pt_BB",
    LEGEND_LABEL_EC1: "h_resp_pt_EC1",
    LEGEND_LABEL_EC2: "h_resp_pt_EC2",
    LEGEND_LABEL_HF:  "h_resp_pt_HF",
}

HIST_FIG10B_RAW = {
    LEGEND_LABEL_BB + " (raw)":  "h_resp_raw_pt_BB",
    LEGEND_LABEL_EC1 + " (raw)": "h_resp_raw_pt_EC1",
    LEGEND_LABEL_EC2 + " (raw)": "h_resp_raw_pt_EC2",
    LEGEND_LABEL_HF + " (raw)":  "h_resp_raw_pt_HF",
}

# ------------------------------------------------------------
# Figure 10(b): displayed pT range
# ------------------------------------------------------------
USE_PT_RANGE_FIG10B = True
XMIN_FIG10B = 20.0
XMAX_FIG10B = 2000.0

# Axis range for Figure 10(b)
YMIN_FIG10B = 0.5
YMAX_FIG10B = 1.5

# Legend box for Figure 10(b)
LEG2_X1 = 0.50
LEG2_Y1 = 0.15
LEG2_X2 = 0.88
LEG2_Y2 = 0.35

# Reference line for Figure 10(b)
REFLINE_FIG10B_XMIN = 20.0
REFLINE_FIG10B_XMAX = 2000.0
REFLINE_FIG10B_Y    = 1.0

# ------------------------------------------------------------
# Global text style
# ------------------------------------------------------------
TEXT_SIZE_HEADER    = 0.040
TEXT_SIZE_LEGEND    = 0.035
AXIS_TITLE_SIZE     = 0.045
AXIS_LABEL_SIZE     = 0.040
Y_TITLE_OFFSET      = 1.25

# ------------------------------------------------------------
# Figure 10(a) style map
#
# 10 GeV   = green, filled circle
# 30 GeV   = black, open circle
# 100 GeV  = yellow, filled square
# 400 GeV  = blue, open square
# 2000 GeV = red, filled triangle
# ------------------------------------------------------------
COLOR_10   = ROOT.kGreen + 2
MARKER_10  = 20

COLOR_30   = ROOT.kBlack
MARKER_30  = 24

COLOR_100  = ROOT.kYellow + 1
MARKER_100 = 21

COLOR_400  = ROOT.kBlue + 1
MARKER_400 = 25

COLOR_2000  = ROOT.kRed + 1
MARKER_2000 = 22

LINEWIDTH_A   = 1
MARKERSIZE_A  = 1.2

STYLE_FIG10A = {
    LEGEND_LABEL_10:   (COLOR_10,   MARKER_10),
    LEGEND_LABEL_30:   (COLOR_30,   MARKER_30),
    LEGEND_LABEL_100:  (COLOR_100,  MARKER_100),
    LEGEND_LABEL_400:  (COLOR_400,  MARKER_400),
    LEGEND_LABEL_2000: (COLOR_2000, MARKER_2000),
}

# ------------------------------------------------------------
# Figure 10(b) style map
# ------------------------------------------------------------
COLOR_BB   = ROOT.kBlack
MARKER_BB  = 20

COLOR_EC1  = ROOT.kRed + 1
MARKER_EC1 = 21

COLOR_EC2  = ROOT.kBlue + 1
MARKER_EC2 = 22

COLOR_HF   = ROOT.kGreen + 2
MARKER_HF  = 23

LINEWIDTH_B   = 1
MARKERSIZE_B  = 1.2

STYLE_FIG10B = {
    LEGEND_LABEL_BB:  (COLOR_BB,  MARKER_BB),
    LEGEND_LABEL_EC1: (COLOR_EC1, MARKER_EC1),
    LEGEND_LABEL_EC2: (COLOR_EC2, MARKER_EC2),
    LEGEND_LABEL_HF:  (COLOR_HF,  MARKER_HF),
}

STYLE_FIG10B_RAW = {
    LEGEND_LABEL_BB + " (raw)":  (COLOR_BB,  24),
    LEGEND_LABEL_EC1 + " (raw)": (COLOR_EC1, 25),
    LEGEND_LABEL_EC2 + " (raw)": (COLOR_EC2, 26),
    LEGEND_LABEL_HF + " (raw)":  (COLOR_HF,  27),
}

# ------------------------------------------------------------
# Reference-line style
# ------------------------------------------------------------
REFLINE_COLOR = ROOT.kGray + 2
REFLINE_STYLE = 2

# ============================================================
# Helper functions
# ============================================================

def ensure_output_dir(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def get_tnamed_title(root_file, name, default="unknown"):
    obj = root_file.Get(name)
    if not obj:
        return default
    try:
        return obj.GetTitle()
    except Exception:
        return default


def style_hist(h, color, marker, linewidth, markersize, linestyle=1):
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(markersize)
    h.SetLineWidth(linewidth)
    h.SetLineStyle(linestyle)


def style_graph(g, color, marker, linewidth, markersize, linestyle=1):
    g.SetLineColor(color)
    g.SetMarkerColor(color)
    g.SetMarkerStyle(marker)
    g.SetMarkerSize(markersize)
    g.SetLineWidth(linewidth)
    g.SetLineStyle(linestyle)


def setup_canvas(name, title):
    c = ROOT.TCanvas(name, title, CANVAS_WIDTH, CANVAS_HEIGHT)
    c.SetLeftMargin(LEFT_MARGIN)
    c.SetRightMargin(RIGHT_MARGIN)
    c.SetBottomMargin(BOTTOM_MARGIN)
    c.SetTopMargin(TOP_MARGIN)
    c.SetTicks(1, 1)
    return c


def apply_axis_style(axis_object, x_title, y_title):
    axis_object.GetXaxis().SetTitle(x_title)
    axis_object.GetYaxis().SetTitle(y_title)

    axis_object.GetXaxis().SetTitleSize(AXIS_TITLE_SIZE)
    axis_object.GetYaxis().SetTitleSize(AXIS_TITLE_SIZE)

    axis_object.GetXaxis().SetLabelSize(AXIS_LABEL_SIZE)
    axis_object.GetYaxis().SetLabelSize(AXIS_LABEL_SIZE)

    axis_object.GetYaxis().SetTitleOffset(Y_TITLE_OFFSET)


def draw_header_and_subheader(header, subheader):
    latex = ROOT.TLatex()
    latex.SetNDC(True)
    latex.SetTextSize(TEXT_SIZE_HEADER)
    latex.DrawLatex(HEADER_X, HEADER_Y, header)
    latex.DrawLatex(SUBHEADER_X, HEADER_Y, subheader)
    return latex


def draw_eta_regions(ymin, ymax):
    lines = []
    labels = []

    if DRAW_ETA_REGION_LINES:
        for x in [
            ETA_BOUNDARY_BB_EC1,
            ETA_BOUNDARY_EC1_EC2,
            ETA_BOUNDARY_EC2_HF,
            ETA_BOUNDARY_HF_END,
        ]:
            line = ROOT.TLine(x, ymin, x, ymax)
            line.SetLineColor(ETA_REGION_LINE_COLOR)
            line.SetLineStyle(ETA_REGION_LINE_STYLE)
            line.SetLineWidth(ETA_REGION_LINE_WIDTH)
            line.Draw()
            lines.append(line)

    if DRAW_ETA_REGION_LABELS:
        latex = ROOT.TLatex()
        latex.SetTextSize(0.030)

        latex.DrawLatex(ETA_LABEL_BB_X,  ETA_LABEL_Y, ETA_LABEL_BB)
        latex.DrawLatex(ETA_LABEL_EC1_X, ETA_LABEL_Y, ETA_LABEL_EC1)
        latex.DrawLatex(ETA_LABEL_EC2_X, ETA_LABEL_Y, ETA_LABEL_EC2)
        latex.DrawLatex(ETA_LABEL_HF_X,  ETA_LABEL_Y, ETA_LABEL_HF)

        labels.append(latex)

    return lines, labels


def hist_to_graph_in_xrange(hist, xmin_keep, xmax_keep, name):
    """
    Convert histogram to TGraphErrors, keeping only points with
    bin centers inside [xmin_keep, xmax_keep].

    This is preferable to zeroing bins because it avoids artificial
    zero-valued points and line artefacts.
    """
    g = ROOT.TGraphErrors()
    g.SetName(name)

    ipoint = 0
    for ibin in range(1, hist.GetNbinsX() + 1):
        x = hist.GetBinCenter(ibin)
        y = hist.GetBinContent(ibin)
        ey = hist.GetBinError(ibin)

        if x < xmin_keep or x > xmax_keep:
            continue

        if not math.isfinite(y):
            continue

        # Skip empty / invalid ratio bins
        if y <= 0.0:
            continue

        ex = hist.GetBinWidth(ibin) / 2.0

        g.SetPoint(ipoint, x, y)
        g.SetPointError(ipoint, ex, ey)
        ipoint += 1

    return g


def load_histograms(root_file, mapping):
    hists = {}
    for label, hist_name in mapping.items():
        h = root_file.Get(hist_name)
        if not h:
            raise KeyError(f"Missing histogram '{hist_name}' for label '{label}'")
        hists[label] = h
    return hists


# ============================================================
# Prepare output directories
# ============================================================

for output_path in [
    OUTPUT_FIG10A_PDF,
    OUTPUT_FIG10A_PNG,
    OUTPUT_FIG10B_PDF,
    OUTPUT_FIG10B_PNG,
    OUTPUT_FIG10B_RAW_PDF,
    OUTPUT_FIG10B_RAW_PNG,
]:
    ensure_output_dir(output_path)

# ============================================================
# Open file and read metadata
# ============================================================

f = ROOT.TFile.Open(INPUT_FILE)
if not f or f.IsZombie():
    raise OSError(f"Could not open file: {INPUT_FILE}")

FIG10A_RECO_PT_MODE = get_tnamed_title(f, "FIG10A_RECO_PT_MODE", "unknown")
MATCH_DR_MAX        = get_tnamed_title(f, "MATCH_DR_MAX", "0.25")
JET_ETA_MAX         = get_tnamed_title(f, "JET_ETA_MAX", "5.2")
USE_EVENT_CLEANING  = get_tnamed_title(f, "USE_EVENT_CLEANING", "unknown")

SUBHEADER_FIG10A = SUBHEADER_FIG10A_BASE
if SHOW_METADATA_IN_FIG10A_HEADER:
    SUBHEADER_FIG10A += f", p_{{T}} source: {FIG10A_RECO_PT_MODE}"

SUBHEADER_FIG10B = SUBHEADER_FIG10B_BASE
if SHOW_METADATA_IN_FIG10B_HEADER:
    SUBHEADER_FIG10B += f", event cleaning: {USE_EVENT_CLEANING}"

# ============================================================
# Figure 10(a)
# ============================================================

hists_a_raw = load_histograms(f, HIST_FIG10A)

graphs_a = {}

for label, hist in hists_a_raw.items():
    if USE_PER_CURVE_ETA_LIMITS:
        xmin_keep, xmax_keep = ETA_RANGE_BY_CURVE[label]
    else:
        xmin_keep, xmax_keep = XMIN_FIG10A, XMAX_FIG10A

    graph = hist_to_graph_in_xrange(
        hist,
        xmin_keep,
        xmax_keep,
        f"{hist.GetName()}_graph",
    )

    color, marker = STYLE_FIG10A[label]
    style_graph(graph, color, marker, LINEWIDTH_A, MARKERSIZE_A)

    graphs_a[label] = graph

c1 = setup_canvas("c_fig10a", "Figure 10(a)")

frame_a = c1.DrawFrame(XMIN_FIG10A, YMIN_FIG10A, XMAX_FIG10A, YMAX_FIG10A)
frame_a.SetTitle(TITLE_FIG10A)
apply_axis_style(frame_a, XLABEL_FIG10A, YLABEL_FIG10A)

# Draw graphs
for label in [
    LEGEND_LABEL_10,
    LEGEND_LABEL_30,
    LEGEND_LABEL_100,
    LEGEND_LABEL_400,
    LEGEND_LABEL_2000,
]:
    graphs_a[label].Draw("P SAME")

# Region markers
eta_lines, eta_labels = draw_eta_regions(YMIN_FIG10A, YMAX_FIG10A)

# Reference line
line1 = ROOT.TLine(XMIN_FIG10A, REFLINE_FIG10A_Y, XMAX_FIG10A, REFLINE_FIG10A_Y)
line1.SetLineStyle(REFLINE_STYLE)
line1.SetLineColor(REFLINE_COLOR)
line1.Draw()

# Legend
leg1 = ROOT.TLegend(LEG1_X1, LEG1_Y1, LEG1_X2, LEG1_Y2)
leg1.SetBorderSize(0)
leg1.SetFillStyle(0)
leg1.SetTextSize(TEXT_SIZE_LEGEND)

for label in [
    LEGEND_LABEL_10,
    LEGEND_LABEL_30,
    LEGEND_LABEL_100,
    LEGEND_LABEL_400,
    LEGEND_LABEL_2000,
]:
    leg1.AddEntry(graphs_a[label], label, "lep")

leg1.Draw()

latex1 = draw_header_and_subheader(HEADER_FIG10A, SUBHEADER_FIG10A)

c1.SaveAs(OUTPUT_FIG10A_PDF)
c1.SaveAs(OUTPUT_FIG10A_PNG)

# ============================================================
# Figure 10(b): corrected response
# ============================================================

hists_b = load_histograms(f, HIST_FIG10B)

for label, hist in hists_b.items():
    color, marker = STYLE_FIG10B[label]
    style_hist(hist, color, marker, LINEWIDTH_B, MARKERSIZE_B)

c2 = setup_canvas("c_fig10b", "Figure 10(b)")
c2.SetLogx()

first_b = hists_b[LEGEND_LABEL_BB]
first_b.SetTitle(TITLE_FIG10B)
apply_axis_style(first_b, XLABEL_FIG10B, YLABEL_FIG10B)

first_b.SetMinimum(YMIN_FIG10B)
first_b.SetMaximum(YMAX_FIG10B)

if USE_PT_RANGE_FIG10B:
    first_b.GetXaxis().SetRangeUser(XMIN_FIG10B, XMAX_FIG10B)

first_b.Draw("E1")

for label in [LEGEND_LABEL_EC1, LEGEND_LABEL_EC2, LEGEND_LABEL_HF]:
    hists_b[label].Draw("E1 SAME")

line2 = ROOT.TLine(
    REFLINE_FIG10B_XMIN,
    REFLINE_FIG10B_Y,
    REFLINE_FIG10B_XMAX,
    REFLINE_FIG10B_Y,
)
line2.SetLineStyle(REFLINE_STYLE)
line2.SetLineColor(REFLINE_COLOR)
line2.Draw()

leg2 = ROOT.TLegend(LEG2_X1, LEG2_Y1, LEG2_X2, LEG2_Y2)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
leg2.SetTextSize(TEXT_SIZE_LEGEND)

for label in [LEGEND_LABEL_BB, LEGEND_LABEL_EC1, LEGEND_LABEL_EC2, LEGEND_LABEL_HF]:
    leg2.AddEntry(hists_b[label], label, "lep")

leg2.Draw()

latex2 = draw_header_and_subheader(HEADER_FIG10B, SUBHEADER_FIG10B)

c2.SaveAs(OUTPUT_FIG10B_PDF)
c2.SaveAs(OUTPUT_FIG10B_PNG)

# ============================================================
# Figure 10(b): raw response comparison
# ============================================================

hists_b_raw = load_histograms(f, HIST_FIG10B_RAW)

for label, hist in hists_b_raw.items():
    color, marker = STYLE_FIG10B_RAW[label]
    style_hist(hist, color, marker, LINEWIDTH_B, MARKERSIZE_B, linestyle=2)

c3 = setup_canvas("c_fig10b_raw", "Figure 10(b) raw")
c3.SetLogx()

first_raw = hists_b_raw[LEGEND_LABEL_BB + " (raw)"]
first_raw.SetTitle(TITLE_FIG10B)
apply_axis_style(first_raw, XLABEL_FIG10B, YLABEL_FIG10B)

first_raw.SetMinimum(YMIN_FIG10B)
first_raw.SetMaximum(YMAX_FIG10B)

if USE_PT_RANGE_FIG10B:
    first_raw.GetXaxis().SetRangeUser(XMIN_FIG10B, XMAX_FIG10B)

first_raw.Draw("E1")

for label in [
    LEGEND_LABEL_EC1 + " (raw)",
    LEGEND_LABEL_EC2 + " (raw)",
    LEGEND_LABEL_HF + " (raw)",
]:
    hists_b_raw[label].Draw("E1 SAME")

line3 = ROOT.TLine(
    REFLINE_FIG10B_XMIN,
    REFLINE_FIG10B_Y,
    REFLINE_FIG10B_XMAX,
    REFLINE_FIG10B_Y,
)
line3.SetLineStyle(REFLINE_STYLE)
line3.SetLineColor(REFLINE_COLOR)
line3.Draw()

leg3 = ROOT.TLegend(LEG2_X1, LEG2_Y1, LEG2_X2, LEG2_Y2)
leg3.SetBorderSize(0)
leg3.SetFillStyle(0)
leg3.SetTextSize(TEXT_SIZE_LEGEND)

for label in [
    LEGEND_LABEL_BB + " (raw)",
    LEGEND_LABEL_EC1 + " (raw)",
    LEGEND_LABEL_EC2 + " (raw)",
    LEGEND_LABEL_HF + " (raw)",
]:
    leg3.AddEntry(hists_b_raw[label], label, "lep")

leg3.Draw()

latex3 = draw_header_and_subheader(
    HEADER_FIG10B,
    SUBHEADER_FIG10B_BASE + " before JEC / raw p_{T}",
)

c3.SaveAs(OUTPUT_FIG10B_RAW_PDF)
c3.SaveAs(OUTPUT_FIG10B_RAW_PNG)

# ============================================================
# Finish
# ============================================================

print("Saved:")
print(f"  {OUTPUT_FIG10A_PDF}")
print(f"  {OUTPUT_FIG10A_PNG}")
print(f"  {OUTPUT_FIG10B_PDF}")
print(f"  {OUTPUT_FIG10B_PNG}")
print(f"  {OUTPUT_FIG10B_RAW_PDF}")
print(f"  {OUTPUT_FIG10B_RAW_PNG}")

print("Metadata read from ROOT file:")
print(f"  FIG10A_RECO_PT_MODE = {FIG10A_RECO_PT_MODE}")
print(f"  MATCH_DR_MAX        = {MATCH_DR_MAX}")
print(f"  JET_ETA_MAX         = {JET_ETA_MAX}")
print(f"  USE_EVENT_CLEANING  = {USE_EVENT_CLEANING}")

f.Close()