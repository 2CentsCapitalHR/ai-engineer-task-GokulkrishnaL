import gradio as gr
from analyze import analyze_documents

def process_docs(files):
    # gradio sends list of temp file objects; pass to analyze_documents
    reviewed_path, summary = analyze_documents(files)
    return reviewed_path, summary

iface = gr.Interface(
    fn=process_docs,
    inputs=gr.Files(file_types=[".docx"]),
    outputs=[gr.File(label="Reviewed DOCX"), gr.JSON(label="Analysis Summary")],
    title="ADGM Corporate Agent",
    description="Upload your incorporation/legal documents for ADGM compliance review."
)

if __name__ == "__main__":
    iface.launch()
