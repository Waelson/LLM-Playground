import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

# Configuração para permitir fallback em dispositivos MPS (Macs com chip Apple Silicon)
# os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# 1️⃣ Carrega o modelo e o tokenizer
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

# 2️⃣ Função de geração de texto
def generate_response(prompt, temperature, top_k, top_p, max_length):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 3️⃣ Cria a interface Gradio
interface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Digite sua pergunta aqui..."),
        gr.Slider(0.1, 1.5, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(10, 100, value=50, step=5, label="Top-K"),
        gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="Top-P"),
        gr.Slider(32, 512, value=128, step=16, label="Max Length"),
    ],
    outputs=gr.Textbox(label="Resposta do Modelo"),
    title="🧠 LLM Playground",
    description="Experimente diferentes parâmetros de inferência e veja como mudam as respostas do modelo."
)

# 4️⃣ Executa o app
if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)
