from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Load tokenizer and model
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load and preprocess dataset
dataset = load_dataset('csv', data_files='task_breakdown_data.csv')

def preprocess(example):
    input_text = "breakdown task: " + example["input"]
    target_text = example["output"]
    model_inputs = tokenizer(input_text, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(target_text, max_length=256, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset["train"].map(preprocess, remove_columns=dataset["train"].column_names)

# Training arguments
training_args = TrainingArguments(
    output_dir="./t5_task_breakdown_model",
    evaluation_strategy="no",
    per_device_train_batch_size=4,
    num_train_epochs=5,
    save_total_limit=2,
    logging_steps=10,
    save_steps=100,
    learning_rate=3e-4,
    report_to="none",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

# Fine-tune the model
trainer.train()

# Save the final model
trainer.save_model("./t5_task_breakdown_model")
tokenizer.save_pretrained("./t5_task_breakdown_model")
