import openai
import re

openai.api_key = ''

def filter_resumes_with_chatgpt(resumes, position, experience):
    selected_candidates = []

    for resume_data in resumes:
        resume_text = resume_data["text"]

        # Формируем запрос для ChatGPT, чтобы он сразу отфильтровал кандидатов по опыту
        prompt = (
            f"Проанализируй резюме кандидата и проверь, подходит ли он для позиции '{position}' "
            f"с опытом работы более чем {experience} лет. "
            f"Если кандидат не соответствует минимальному опыту, ответь 'Не подходит'. "
            f"Если подходит, верни информацию в формате:\n"
            f"ФИО: [имя]\nВозраст: [возраст]\nОбразование: [образование]\n"
            f"Телефон: [номер телефона]\nГород: [город]\nОпыт работы: [опыт].\n\n"
            f"Резюме:\n{resume_text}"
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )

            result = response.choices[0].message.content.strip()
            print(result)  # Для отладки, чтобы видеть ответ ChatGPT

            # Проверяем ответ: если "Не подходит", то пропускаем резюме
            if "Не подходит" in result:
                continue

            # Если кандидат подходит, разбираем ответ
            candidate_data = parse_candidate_data(result)
            selected_candidates.append(candidate_data)

        except openai.OpenAIError as e:
            print(f"Ошибка при запросе к API: {e}")

    return selected_candidates


def parse_candidate_data(response_text):
    """Извлекает данные кандидата из ответа ChatGPT и преобразует их в словарь."""
    candidate = {}

    name_match = re.search(r"ФИО:\s*(.*)", response_text)
    age_match = re.search(r"Возраст:\s*(\d+)", response_text)
    education_match = re.search(r"Образование:\s*(.*)", response_text)
    phone_match = re.search(r"Телефон:\s*(.*)", response_text)
    city_match = re.search(r"Город:\s*(.*)", response_text)
    experience_match = re.search(r"Опыт работы:\s*(\d+)", response_text)

    candidate["name"] = name_match.group(1) if name_match else "Не указано"
    candidate["age"] = int(age_match.group(1)) if age_match else None
    candidate["education"] = education_match.group(1) if education_match else "Не указано"
    candidate["phone"] = phone_match.group(1) if phone_match else "Не указано"
    candidate["city"] = city_match.group(1) if city_match else "Не указан"
    candidate["experience"] = int(experience_match.group(1)) if experience_match else 0

    return candidate
