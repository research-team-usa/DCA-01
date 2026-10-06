import sys
sys.path.append("../common")
from lora_trainer import LoRATrainer

class CodeLoRATrainer(LoRATrainer):
    def __init__(self):
        super().__init__(module_id="code_expert", base_model="codellama/CodeLlama-7b-Instruct-hf", rank=16)
    def custom_loss(self, prediction, target):
        return "code_loss: syntax_validity + unit_test_pass_rate"

if __name__ == "__main__":
    trainer = CodeLoRATrainer()
    report = trainer.train("../../audit_logs/dataset_code_failures.jsonl", "../../../models/code")
    print(f"Code LoRA ready: {report}")