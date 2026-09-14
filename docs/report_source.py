"""Create the required short project report as docs/report.pdf."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "report.pdf"


def p(text, style):
    return Paragraph(text, style)


def build() -> None:
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18,
                           leading=22, alignment=TA_CENTER, spaceAfter=5)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=9, leading=12,
                              alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=16)
    h = ParagraphStyle("Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12,
                       leading=15, spaceBefore=10, spaceAfter=5, textColor=colors.black)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4,
                          leading=13, spaceAfter=6)
    small = ParagraphStyle("Small", parent=body, fontSize=8.5, leading=11)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2.0*cm, leftMargin=2.0*cm,
                            topMargin=1.6*cm, bottomMargin=1.6*cm)
    story = [
        p("Checkers Mini AI Adversarial Search", title),
        p("Project report | Student: replace with your name | Register number: replace before submission", subtitle),
        p("1. Problem formulation", h),
        p("The task is to choose a legal move for one side of an 8 by 8 English draughts board. "
          "A state is a board configuration plus the player whose turn it is. An action is a legal diagonal move "
          "or a complete capture sequence. The goal is to force the opponent into a state with no legal moves or no pieces. "
          "The agent treats Black as the maximizing player and Red as the minimizing player.", body),
        p("The essential constraint is compulsory capture. If any piece can jump an opponent, every quiet move is illegal. "
          "If that same piece can jump again after landing, the full chain must be completed in the same turn. Men move forward; kings move in both directions. "
          "A man that reaches the far row is crowned and its turn ends, following the English draughts convention.", body),
        p("2. Approach", h),
        p("The program uses depth-limited minimax with alpha-beta pruning. At each node it calls one shared "
          "<font name='Courier'>legal_moves(board, side)</font> function. This function first collects all capture chains for every piece; it returns those chains when any exist, otherwise it returns quiet diagonal moves. "
          "Consequently, the search tree itself contains only legal continuations and forced captures are respected at every maximizing and minimizing node.", body),
        p("A recursive capture generator removes the jumped piece, moves the capturing piece, and continues from its landing square. "
          "It emits a move only when no further jump is available, so a sequence such as 9x18x27 is one action rather than two optional actions. "
          "Move ordering tries captures and longer chains first to help alpha-beta prune earlier.", body),
        p("The evaluation is from the AI's perspective. It combines material (100 per man), king value (an additional 75), a small promotion-progress bonus for men, centre occupancy, and mobility. "
          "A terminal no-move state receives a score of plus or minus 100,000, which dominates heuristic values.", body),
        p("3. Complexity", h),
        p("With branching factor b and search depth d, plain minimax is O(b^d) time and O(d) recursion space, excluding stored boards. "
          "Alpha-beta has the same worst case but approaches O(b^(d/2)) with excellent ordering. Checkers branching is position-dependent: forced captures often reduce b sharply, while multi-jumps make one action longer to generate. "
          "The demonstration defaults to depth 5 to stay responsive without a transposition table.", body),
        PageBreak(),
        p("4. Results", h),
    ]
    data = [
        [p("Check", small), p("Expected result", small), p("Observed result", small)],
        [p("Initial board", small), p("Seven Black opening moves", small), p("Pass", small)],
        [p("Forced capture", small), p("Quiet moves excluded when a jump exists", small), p("Pass", small)],
        [p("Multi-jump", small), p("9x18x27 generated as one action", small), p("Pass", small)],
        [p("Search legality", small), p("Alpha-beta chooses 9x18 in forced position", small), p("Pass", small)],
        [p("Evaluation", small), p("Extra own piece increases score", small), p("Pass", small)],
    ]
    table = Table(data, colWidths=[3.0*cm, 8.0*cm, 2.4*cm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9D9D9")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F5F8FC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [table, p("5. Reflection", h),
              p("The difficult part was representing a turn as an entire capture chain while still keeping the rules simple for search. "
                "Using one legal-move generator prevented the UI and agent from disagreeing about compulsory captures. A next improvement would add iterative deepening, transposition tables, and stronger positional features. "
                "Honesty note: AI assistance was used to help draft and implement this project; the submitted student should understand and be able to explain the design.", body),
              p("6. Demonstration evidence", h),
              p("The automated tests are run with <font name='Courier'>python -m unittest discover -s tests -v</font>. "
                "The command reports five passing tests. The command-line demonstration is run with "
                "<font name='Courier'>python -m src.game --depth 5</font>. It prints the board and the selected move after each turn. "
                "When a capture becomes available, the displayed legal move is written with x notation rather than a quiet move with a hyphen.", body),
              p("For the key forced-capture test, Black has a jump from square 9 over Red's piece on square 14 to square 18, while a different Black piece also has a quiet move. "
                "The legal-move list contains only 9x18, and the alpha-beta agent selects that capture. In the multi-jump test, Black's only action is 9x18x27; both jumped Red pieces disappear after applying the single returned move.", body),
              p("7. Limitations", h),
              p("This is an educational mini-agent rather than a tournament engine. It has no opening book, endgame database, draw-by-repetition detection, or transposition table. "
                "The evaluation is deliberately interpretable instead of learned. These choices keep the implementation compact while making the adversarial-search and forced-capture behaviour easy to inspect and defend.", body)]
    doc.build(story)


if __name__ == "__main__":
    build()
