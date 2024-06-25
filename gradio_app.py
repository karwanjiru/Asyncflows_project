import os
from pathlib import Path
import gradio as gr
import asyncio
import pandas as pd
from asyncflows import AsyncFlows
from asyncflows.utils.async_utils import merge_iterators
from asyncflows.log_config import get_logger

with gr.Blocks() as demo:
    file_upload = gr.File(label="Upload Patient File", type="filepath")
    submit_button = gr.Button("Analyze")

    with gr.Row():
        personal_info = gr.Textbox(label="Personal Information", interactive=False)
        medical_history = gr.Textbox(label="Medical History", interactive=False)
        clinical_notes = gr.Textbox(label="Clinical Notes", interactive=False)
        diagnosis = gr.Textbox(label="Diagnosis", interactive=False)
        treatment_plans = gr.Textbox(label="Treatment Plans", interactive=False)
        progress_reports = gr.Textbox(label="Progress Reports", interactive=False)
        consent_forms = gr.Textbox(label="Consent Forms", interactive=False)
        adm_info = gr.Textbox(label="Administrative Information", interactive=False)
        legal_doc = gr.Textbox(label="Legal Documentation", interactive=False)
        bill_info = gr.Textbox(label="Financial Information", interactive=False)
        misc = gr.Textbox(label="Miscellaneous", interactive=False)
    
    analysis = gr.Textbox(label="Analysis (synthesis)", interactive=False)

    async def handle_submit(file_path):
        # Read the contents of the uploaded file
        with open(file_path, 'r') as f:
            query = f.read()

        # Clear the output fields
        yield {
            personal_info: "",
            medical_history: "",
            clinical_notes: "",
            diagnosis: "",
            treatment_plans: "",
            progress_reports: "",
            consent_forms: "",
            adm_info: "",
            legal_doc: "",
            bill_info: "",
            misc: "",
            analysis: "",
        }

        # Load the chatbot flow
        flow = AsyncFlows.from_file("project.yaml").set_vars(
            query=query,
        )

        log = get_logger()

        # Stream the docs
        async for doc, outputs in merge_iterators(
            log,
            [
                personal_info,
                medical_history,
                clinical_notes,
                diagnosis,
                treatment_plans,
                progress_reports,
                consent_forms,
                adm_info,
                legal_doc,
                bill_info,
                misc
            ],
            [
                flow.stream('personal_info.result'),
                flow.stream('medical_history.result'),
                flow.stream('clinical_notes.result'),
                flow.stream('diagnosis.result'),
                flow.stream('treatment_plans.result'),
                flow.stream('progress_reports.result'),
                flow.stream('consent_forms.result'),
                flow.stream('adm_info.result'),
                flow.stream('legal_doc.result'),
                flow.stream('bill_info.result'),
                flow.stream('misc.result'),
            ],
        ):
            yield {
                doc: outputs
            }

        # Stream the analysis
        async for outputs in flow.stream("analysis.result"):
            yield {
                analysis: outputs
            }

    submit_button.click(
        fn=handle_submit,
        inputs=[file_upload],
        outputs=[
            personal_info,
            medical_history,
            clinical_notes,
            diagnosis,
            treatment_plans,
            progress_reports,
            consent_forms,
            adm_info,
            legal_doc,
            bill_info,
            misc,
            analysis,
        ],
    )

if __name__ == "__main__":
    demo.launch()
