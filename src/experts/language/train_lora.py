import sys
sys.path.append("../common")
from lora_trainer import LoRATrainer

class LanguageLoRATrainer(LoRATrainer):
    def __init__(self):
        super().__init__(module_id="language_expert", base_model="meta-llama/Llama-3-8B-Instruct", rank=8)

if __name__ == "__main__":
    trainer = LanguageLoRATrainer()
    report = trainer.train("../../audit_logs/dataset_language_failures.jsonl", "../../../models/language")
    print(f"Language LoRA ready: {report}")