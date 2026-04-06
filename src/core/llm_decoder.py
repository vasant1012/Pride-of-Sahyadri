from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class JSONToTextGenerator:
    def __init__(self, model_name="google/flan-t5-base", max_length=1000):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.max_length = max_length

    def fort_dict_to_paragraph(self, data: dict) -> str:
        return (
            f"{data['name']} is a {data['type']} located in "  # NOQA E501
            f"{data['taluka']}, {data['district']} district. It was built by "
            f"{data['built_by']} during the {data['era']} around {data['year_of_construction']}. "  # NOQA E501
            f"The fort stands at an elevation of about {data['elevation_m']} meters above sea level "  # NOQA E501
            f"and is currently in a {data['current_condition']} condition. "
            f"Historically, it served as {data['key_events']}. "
            f"The base village for the fort is {data['base_village']}, situated at latitude "  # NOQA E501
            f"{data['latitude']} and longitude {data['longitude']}. "
            f"The trek to the fort is considered {data['trek_difficulty']} and generally takes "  # NOQA E501
            f"around {data['trek_time_hours']} hour(s). The best season to visit the fort is during "  # NOQA E501
            f"{data['best_season']}. Water availability at the fort includes {data['water_availability']}, "  # NOQA E501
            f"and accommodation options are available in {data['accommodation']}. "  # NOQA E501
            f"The fort is an ASI-protected site: {data['asi_protected']}. "
            f"Additional notes: {data['notes']}"
        )

    def answer(self, context: str, question: str) -> str:
        prompt = (
            f"Use the context to answer the question.\n\n"
            f"Read the context : {context}\n\n"
            f"Understand the question: {question}\n"
            "and write ONE COMPLETE ANSWER that clearly summarizes it."
            "Do not answer in short phrases. Write a full sentence with proper grammar:\n\n"  # NOQA E501
            f"Answer:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        output = self.model.generate(
            **inputs,
            max_length=120,
            num_beams=5,
            repetition_penalty=1.2,
            early_stopping=True
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
