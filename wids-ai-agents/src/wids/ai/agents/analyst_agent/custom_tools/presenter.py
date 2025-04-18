import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


class Presenter:
    def __init__(self, theme_path: str = "presenter_theme.pptx"):
        self.theme_path = theme_path
        self.prs = Presentation(theme_path) if theme_path and os.path.exists(theme_path) else Presentation()


    def add_content_slide(self, title_text: str, content_text: str, bg_color: RGBColor = RGBColor(255, 255, 255)):
        """Adds a slide with title, content, and background color."""
        slide_layout = self.prs.slide_layouts.get_by_name("TITLE_AND_BODY") # Title and Content Layout
        slide = self.prs.slides.add_slide(slide_layout)
        # set_slide_background(slide, bg_color)

        title = slide.shapes.title
        title.text = title_text
        title.text_frame.paragraphs[0].font.bold = True
        title.text_frame.paragraphs[0].font.size = Pt(32)

        # Content Text Box
        # print(len(slide.placeholders))
        print(slide.placeholders[1].placeholder_format.idx)
        for placeholder in slide.placeholders:
            print(placeholder.placeholder_format.idx)
        text_frame = slide.placeholders[1].text_frame
        text_frame.word_wrap = True
        # text_frame.text = content_text
        
        # text_frame.word_wrap = True

        for paragraph in content_text.split("\n"):
            p = text_frame.add_paragraph()
            p.text = paragraph
            p.font.size = Pt(20)
            # p.font.color = RGBColor(255, 255, 255)

    # Function to Add Image Slide
    def add_image_slide(self, title_text: str, img_path: str):
        """Adds a slide with an image."""
        slide_layout = self.prs.slide_layouts.get_by_name("TITLE_ONLY")  # Title Only Layout
        slide = self.prs.slides.add_slide(slide_layout)

        title = slide.shapes.title
        title.text = title_text

        left = Inches(1)
        top = Inches(1.5)
        width = Inches(8)
        slide.shapes.add_picture(img_path, left, top, width=width)

    # Function to Generate Histograms
    def generate_histogram(self, data, column, filename):
        """Generates and saves a histogram for a given column."""
        plt.figure(figsize=(6, 4))
        data[column].hist(bins=20, color="skyblue", edgecolor="black")
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.grid(False)
        plt.savefig(filename, bbox_inches="tight")
        plt.close()

    # Function to Generate Correlation Heatmap
    def generate_correlation_heatmap(self, data, filename):
        """Generates and saves a correlation heatmap."""
        plt.figure(figsize=(6, 4))
        sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Feature Correlation Heatmap")
        plt.savefig(filename, bbox_inches="tight")
        plt.close()

    # Function to Generate Box Plots
    def generate_boxplot(self, data, column, filename):
        """Generates and saves a box plot for a given column."""
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=data[column], color="lightblue")
        plt.title(f"{column} Box Plot")
        plt.savefig(filename, bbox_inches="tight")
        plt.close()

def generate_presentation(content: str, theme_path: str = "presenter_theme.pptx"):
    """
    Build a PowerPoint presentation with a background theme.

    Args:
        content: Text content to include in the presentation.
        theme_path: (Optional) Path to a PowerPoint theme/template (.pptx) file.
    """
  
    try:
        # Load Presentation Theme (Optional)
        # theme_path = None  # Provide a theme path if available
        agent = Presenter(theme_path)
        prs = agent.prs
        print(prs.slide_layouts)


        # Load AI Agent Data
        df = pd.read_csv("/Users/michellerojas/pydata/virginia2025/wids-demo-agent/wids-ai-agents/src/wids/ai/agents/analyst_agent/diabetes.csv")  # Replace with actual dataset

        # --- STEP 1: ADD TITLE SLIDE ---
        title_slide_layout = prs.slide_layouts.get_by_name("TITLE")
        
        slide = prs.slides.add_slide(title_slide_layout)
        slide.shapes.title.text = "AI Agent for Diabetes Prediction"
        print(slide.placeholders)
        slide.placeholders[1].text = "Machine Learning Workflow & Insights"

        # --- STEP 2: ADD CONTENT SLIDES ---
        content_slides = """
        This AI Agent predicts diabetes based on patient health records.
        It uses machine learning to classify high-risk patients.
        Steps in the workflow:
        1. Data Collection
        2. Data Preprocessing
        3. Feature Engineering
        4. Model Training
        5. Real-Time Predictions
        6. Deployment
        """
        agent.add_content_slide("AI Agent Workflow", content_slides)
        agent.add_content_slide("Results", content)

        # --- STEP 3: ADD EXPLORATORY DATA ANALYSIS (EDA) SLIDES ---
        eda_columns = ["Age", "BMI", "Glucose"]  # Select columns for EDA
        for col in eda_columns:
            hist_img = f"{col}_hist.png"
            agent.generate_histogram(df, col, hist_img)
            agent.add_image_slide(f"{col} Distribution", hist_img)

        # --- STEP 4: ADD CORRELATION HEATMAP ---
        corr_img = "correlation_heatmap.png"
        agent.generate_correlation_heatmap(df, corr_img)
        agent.add_image_slide("Feature Correlation Heatmap", corr_img)

        # --- STEP 5: ADD BOX PLOTS FOR OUTLIERS DETECTION ---
        for col in eda_columns:
            box_img = f"{col}_boxplot.png"
            agent.generate_boxplot(df, col, box_img)
            agent.add_image_slide(f"{col} Box Plot", box_img)

        # Accuracy Slide
        # accuracy_content = f"Model Accuracy: {accuracy:.2%}\n\nHigher accuracy indicates better classification performance."
        # add_content_slide(prs, "Model Accuracy", accuracy_content)

        # # Classification Report Slide
        # class_report_content = "Classification Report:\n"
        # for label, metrics in class_report.items():
        #     if isinstance(metrics, dict):
        #         class_report_content += f"{label}: Precision: {metrics['precision']:.2f}, Recall: {metrics['recall']:.2f}, F1-score: {metrics['f1-score']:.2f}\n"
        # add_content_slide(prs, "Classification Report", class_report_content)

        # # Confusion Matrix Slide
        # plt.figure(figsize=(6, 4))
        # sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
        # plt.xlabel("Predicted")
        # plt.ylabel("Actual")
        # plt.title("Confusion Matrix")
        # conf_matrix_img = "confusion_matrix.png"
        # plt.savefig(conf_matrix_img, bbox_inches="tight")
        # plt.close()
        # add_image_slide(prs, "Confusion Matrix", conf_matrix_img)

        # # Feature Importance Slide
        # feature_importance_content = "Feature Importance:\n"
        # for feature, importance in sorted(feature_importances.items(), key=lambda x: x[1], reverse=True):
        #     feature_importance_content += f"{feature}: {importance:.4f}\n"
        # add_content_slide(prs, "Feature Importance", feature_importance_content)


        # --- SAVE PRESENTATION ---
        file_path = os.path.abspath("ai_agent_presentation_updated_model_2.pptx")
        prs.save(file_path)

        return {
            "status": "success",
            "message": f"Presentation created successfully at {file_path}",
            "file_path": file_path
        }

    except Exception as e:
        print(f"Failed to create presentation: {str(e)}")
        # raise e
        return {
            "status": "error",
            "message": f"Failed to create presentation: {str(e)}"
        }


if __name__ == "__main__":
    generate_presentation()