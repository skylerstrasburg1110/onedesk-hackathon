import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define CSV file path
csv_file_path = "metricsData.csv"

# Ensure the CSV file exists before reading
if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=["Call_ID", "Agent_Name", "Tried_Upsell", "Asked_Reward_Card", "Introduced_Themselves"])
    df.to_csv(csv_file_path, index=False)

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Group by Agent Name and calculate averages
summary = df.groupby("Agent_Name").mean(numeric_only=True)

# Define hardcoded percent changes (Green for positive, Red for negative)
percent_changes = {"overall": 1, "metric_1": 2, "metric_2": 3, "metric_3": -2}

# Define PDF file path
pdf_file_path = "metricsData.pdf"

# Create PDF canvas
c = canvas.Canvas(pdf_file_path, pagesize=letter)
width, height = letter

# Set background color to white (removes any previous colors)
c.setFillColor(colors.white)
c.rect(0, 0, width, height, fill=True, stroke=False)
c.drawImage("photos/logo.png", width - 120, height - 100, width=100, height=100, mask="auto", preserveAspectRatio="True") #test

# Title in black (Removed dark blue bar)
c.setFillColor(colors.black)
c.setFont("Courier-Bold", 18)
c.drawString(180, height - 50, "Performance Report")


# Set initial text position
y_position = height - 80

# Function to color metric scores based on performance
def get_metric_color(score):
    if score >= 85:
        return colors.green  # High performance ✅
    elif 75 <= score < 85:
        return colors.orange  # Moderate performance ⚠️
    else:
        return colors.red  # Low performance ❌

# Generate the report for each agent
for agent, row in summary.iterrows():
    overall_score = round((row["Tried_Upsell"] + row["Asked_Reward_Card"] + row["Introduced_Themselves"]) / 3 * 100, 2)

    # Agent Name in black
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, f"Agent: {agent}")

    # Overall Score with color coding
    c.setFillColor(get_metric_color(overall_score))
    c.drawString(200, y_position, f"Overall Score: {overall_score}%")

    # Change Percentage (Green for positive, Red for negative)
    change_color = colors.green if percent_changes["overall"] > 0 else colors.red
    c.setFillColor(change_color)
    c.drawString(350, y_position, f"Change: {percent_changes['overall']}%")

    y_position -= 20

    # Metric 1 - Upsell
    metric_1_score = round(row["Tried_Upsell"] * 100, 2)
    c.setFillColor(get_metric_color(metric_1_score))
    c.drawString(70, y_position, f"Metric 1 (Upsell) - Score: {metric_1_score}% | Change: {percent_changes['metric_1']}%")
    y_position -= 15

    # Metric 2 - Reward Card
    metric_2_score = round(row["Asked_Reward_Card"] * 100, 2)
    c.setFillColor(get_metric_color(metric_2_score))
    c.drawString(70, y_position, f"Metric 2 (Reward Card) - Score: {metric_2_score}% | Change: {percent_changes['metric_2']}%")
    y_position -= 15
    
    # Metric 3 - Intro
    metric_3_score = round(row["Introduced_Themselves"] * 100, 2)
    c.setFillColor(get_metric_color(metric_3_score))
    c.drawString(70, y_position, f"Metric 3 (Introduced_Themselves) - Score: {metric_3_score}% | Change: {percent_changes['metric_3']}%")
    y_position -= 15
    



    # Separator line to visually break up agents
    c.setStrokeColor(colors.black)
    c.line(50, y_position - 10, width - 100, y_position - 10)
    y_position -= 40

    # Page break if running out of space
    if y_position < 100:
        c.showPage()
        y_position = height - 50



# Save the PDF file
c.save()

# Return the generated PDF file path
pdf_file_path





# c.drawImage("photos/logo.png", -100, -100, width=80, height=80, mask="auto", preserveAspectRatio=True)


# Call_ID,Agent_Name,Tried_Upsell,Asked_Reward_Card,Introduced_Themselves
# 1,Jalen,1,0,1
# 2,Jalen,0,1,1
# 3,Alex,1,1,1
# 4,Jordan,0,0,1
