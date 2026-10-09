# NEOTERIC: Data Science SLM Tutor

## Project Overview
NEOTERIC is a specialized AI teaching assistant designed to help university students grasp complex Data Science, Machine Learning, and Statistics concepts. Instead of relying on closed-source external APIs, NEOTERIC is powered by a custom-fine-tuned Small Language Model (SLM) hosted locally.

## Architecture Stack
* **Model:** Phi-3-mini (3.8B) / Qwen 1.5B (Instruction Tuned via LoRA/QLoRA)
* **Training Framework:** Hugging Face `transformers`, `peft`, `TRL`
* **Backend:** FastAPI (Python) for optimized inference serving
* **Frontend:** React.js for an interactive chat interface

## The "Socratic" Fine-Tuning Strategy
Most LLMs simply output the final answer. NEOTERIC is fine-tuned to act as a *tutor*. When a student asks "How does a Random Forest work?", the model is trained to:
1. Explain the core intuition simply.
2. Provide a brief mathematical or programmatic example.
3. End with a guiding question to check the student's understanding.
