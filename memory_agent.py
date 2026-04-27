import os
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ReportLab imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class MemoryAgent:
    def __init__(self):
        print("💾 System: Initializing Memory Agent...")
        self.save_dir = "generated_reports"
        self.assets_dir = os.path.join(self.save_dir, "assets")
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def _draw_architecture(self, filename):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')

        box_style = dict(boxstyle="round,pad=0.3", fc="#E0E7FF", ec="#4338ca", lw=2)
        arrow_props = dict(facecolor='black', arrowstyle='->', lw=1.5)

        ax.text(5, 5, "User Input", ha="center", va="center", size=10, bbox=dict(boxstyle="round", fc="#f3f4f6"))
        ax.text(5, 3, "COORDINATOR", ha="center", va="center", size=12, weight='bold', bbox=dict(boxstyle="circle,pad=0.5", fc="#c7d2fe", ec="#312e81"))

        ax.text(2, 4, "Search", ha="center", va="center", bbox=box_style)
        ax.text(8, 4, "Analysis", ha="center", va="center", bbox=box_style)
        ax.text(2, 2, "Trend", ha="center", va="center", bbox=box_style)
        ax.text(8, 2, "Citation", ha="center", va="center", bbox=box_style)

        ax.annotate("", xy=(5, 3.8), xytext=(5, 4.7), arrowprops=arrow_props)
        ax.annotate("", xy=(2.6, 3.8), xytext=(4.2, 3.2), arrowprops=arrow_props)
        ax.annotate("", xy=(7.4, 3.8), xytext=(5.8, 3.2), arrowprops=arrow_props)
        ax.annotate("", xy=(2.6, 2.2), xytext=(4.2, 2.8), arrowprops=arrow_props)
        ax.annotate("", xy=(7.4, 2.2), xytext=(5.8, 2.8), arrowprops=arrow_props)

        plt.title("Multi-Agent System Architecture", y=0.05, fontsize=10, style='italic')
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()

    def _draw_charts(self, papers, filename):
        years = [p['date'][:4] for p in papers]
        unique_years = sorted(list(set(years)))
        counts = [years.count(y) for y in unique_years]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(unique_years, counts, color='#312e81', width=0.6)
        plt.title('Analysis of Paper Distribution by Year', fontsize=12)
        plt.ylabel('Number of Papers')
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()

    def _draw_ai_pie_chart(self, ai_score, filename):
        labels = ['AI Generated', 'Human Written']
        sizes = [ai_score, 100 - ai_score]
        colors = ['#6366f1', '#10b981']
        
        plt.figure(figsize=(4, 4))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, 
                wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        plt.title('Content Origin Analysis', fontsize=12)
        plt.tight_layout()
        plt.savefig(filename, dpi=300, transparent=True)
        plt.close()

    def _draw_flowchart(self, filename):
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        box = dict(boxstyle="round,pad=0.5", fc="#f8fafc", ec="#475569", lw=2)
        arrow = dict(facecolor='black', arrowstyle='->', lw=2)
        
        ax.text(5, 9, "1. Query Generation", ha="center", va="center", bbox=box, fontsize=10)
        ax.text(5, 7, "2. ArXiv Extraction (15 Papers)", ha="center", va="center", bbox=box, fontsize=10)
        ax.text(5, 5, "3. Deep LLM Analysis", ha="center", va="center", bbox=box, fontsize=10)
        ax.text(5, 3, "4. Plagiarism & AI Detection", ha="center", va="center", bbox=box, fontsize=10)
        ax.text(5, 1, "5. IEEE PDF Compilation", ha="center", va="center", bbox=box, fontsize=10)
        
        ax.annotate("", xy=(5, 7.5), xytext=(5, 8.5), arrowprops=arrow)
        ax.annotate("", xy=(5, 5.5), xytext=(5, 6.5), arrowprops=arrow)
        ax.annotate("", xy=(5, 3.5), xytext=(5, 4.5), arrowprops=arrow)
        ax.annotate("", xy=(5, 1.5), xytext=(5, 2.5), arrowprops=arrow)
        
        plt.title('Data Processing Pipeline Flowchart', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()


    def save_report_pdf(self, topic, trends_text, papers, citations_text, ai_score, plag_score, project_sections=None):
        if project_sections is None:
            project_sections = {}
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_topic = topic.replace(" ", "_").lower()[:30]
        pdf_filename = f"IEEE_Paper_{clean_topic}_{timestamp}.pdf"
        filepath = os.path.join(self.save_dir, pdf_filename)

        chart_path = os.path.join(self.assets_dir, f"chart_{timestamp}.png")
        diag_path = os.path.join(self.assets_dir, f"diag_{timestamp}.png")
        pie_path = os.path.join(self.assets_dir, f"pie_{timestamp}.png")
        flow_path = os.path.join(self.assets_dir, f"flow_{timestamp}.png")
        
        self._draw_charts(papers, chart_path)
        self._draw_architecture(diag_path)
        self._draw_ai_pie_chart(ai_score, pie_path)
        self._draw_flowchart(flow_path)

        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        
        # Typography: Font: Times New Roman, Headings: 14pt BOLD, Subheadings: 12pt normal, Body: 12pt normal
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Times-Bold',
            fontSize=18,
            alignment=1, # Center
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontName='Times-Bold',
            fontSize=14, 
            spaceBefore=15,
            spaceAfter=10
        )

        subheading_style = ParagraphStyle(
            'SubHeadingStyle',
            parent=styles['Heading3'],
            fontName='Times-Roman',
            fontSize=12,
            spaceBefore=10,
            spaceAfter=5
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontName='Times-Roman', 
            fontSize=12, 
            leading=16, 
            spaceAfter=12
        )
        
        abstract_style = ParagraphStyle(
            'AbstractStyle',
            parent=styles['Normal'],
            fontName='Times-Italic',
            fontSize=12,
            leftIndent=20,
            rightIndent=20,
            leading=16,
            spaceAfter=20
        )

        metrics_style = ParagraphStyle(
            'MetricsStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            alignment=1, # Center
            spaceBefore=10,
            spaceAfter=10
        )

        Story = []

        # 1. Title
        Story.append(Paragraph(topic.upper(), title_style))
        
        # 1. ABSTRACT
        Story.append(Paragraph("1. Abstract", heading_style))
        Story.append(Paragraph(project_sections.get("ABSTRACT", "Abstract content generation pending."), abstract_style))

        # 2. KEYWORDS
        Story.append(Paragraph("2. Keywords", heading_style))
        Story.append(Paragraph("<b>Keywords:</b> Artificial Intelligence, Multi-Agent System, React, Python, Automated Literature Review, LLM.", body_style))
        Story.append(PageBreak())

        # 3. INTRODUCTION
        Story.append(Paragraph("3. Introduction", heading_style))
        Story.append(Paragraph(project_sections.get("INTRODUCTION", "Introduction content generation pending."), body_style))

        # 4. LITERATURE REVIEW (Analyzed Papers)
        Story.append(Paragraph("4. Literature Review", heading_style))
        Story.append(Paragraph("This section reviews the extracted academic papers relevant to the topic.", body_style))
        for idx, paper in enumerate(papers):
            title = paper.get('title', 'Unknown Title').replace('<', '&lt;').replace('>', '&gt;')
            analysis = paper.get('analysis', '').replace('**', '').replace('<', '&lt;').replace('>', '&gt;')
            Story.append(Paragraph(f"4.{idx+1} {title}", subheading_style))
            Story.append(Paragraph(analysis, body_style))
            Story.append(Spacer(1, 0.1*inch))
        Story.append(PageBreak())

        # 5. METHODOLOGY
        Story.append(Paragraph("5. Methodology", heading_style))
        Story.append(Paragraph(project_sections.get("METHODOLOGY", "Methodology content generation pending."), body_style))
        Story.append(Spacer(1, 0.2*inch))
        Story.append(RLImage(flow_path, width=4*inch, height=5.3*inch))
        Story.append(PageBreak())

        # 6. SYSTEM ARCHITECTURE
        Story.append(Paragraph("6. System Architecture", heading_style))
        Story.append(Paragraph("The system relies on a dynamic architecture without a traditional database, executing multi-agent processes in real-time.", body_style))
        Story.append(Spacer(1, 0.1*inch))
        Story.append(RLImage(diag_path, width=5.5*inch, height=3.5*inch))
        Story.append(PageBreak())

        # 7. IMPLEMENTATION
        Story.append(Paragraph("7. Implementation", heading_style))
        Story.append(Paragraph(project_sections.get("IMPLEMENTATION", "Implementation content generation pending."), body_style))

        # 8. RESULTS AND DISCUSSION
        Story.append(Paragraph("8. Results and Discussion", heading_style))
        Story.append(Paragraph("The analysis revealed clear publication trends and metrics regarding AI detection probability.", body_style))
        metrics_text = f"<b>System Execution Metrics:</b><br/>AI Generation Probability: {ai_score}%<br/>Plagiarism Score: {plag_score}%"
        Story.append(Paragraph(metrics_text, body_style))
        Story.append(RLImage(pie_path, width=3*inch, height=3*inch))
        Story.append(Spacer(1, 0.1*inch))
        Story.append(RLImage(chart_path, width=4*inch, height=2.6*inch))
        for p in trends_text.split('\n'):
            if p.strip():
                clean_p = p.replace('**', '').replace('##', '').strip()
                Story.append(Paragraph(clean_p, body_style))
        Story.append(PageBreak())

        # 9. CONCLUSION
        Story.append(Paragraph("9. Conclusion", heading_style))
        Story.append(Paragraph(project_sections.get("CONCLUSION", "Conclusion content generation pending."), body_style))

        # 10. FUTURE SCOPE
        Story.append(Paragraph("10. Future Scope", heading_style))
        Story.append(Paragraph(project_sections.get("FUTURE_SCOPE", "Future scope content generation pending."), body_style))
        Story.append(PageBreak())

        # 11. REFERENCES
        Story.append(Paragraph("11. References", heading_style))
        for p in citations_text.split('\n'):
            if p.strip():
                clean_p = p.replace('**', '').replace('<', '&lt;').replace('>', '&gt;')
                Story.append(Paragraph(clean_p, body_style))

        # Build Document
        def add_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(inch, 0.75 * inch, "Generated by Neural Conductor - AI Research Platform")
            canvas.drawRightString(7.5 * inch, 0.75 * inch, f"Page {doc.page}")
            canvas.restoreState()

        doc.build(Story, onFirstPage=add_footer, onLaterPages=add_footer)
        print(f"✅ IEEE Paper Saved: {filepath}")
        return pdf_filename