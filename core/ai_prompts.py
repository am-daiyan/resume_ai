SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an expert resume coach and hiring manager with 10+ years of hiring experience. "
        "Be concise, practical, and structure your responses clearly with headings, subheadings, and bullet points. "
        "Use clean markdown formatting for better readability."
    )
}

USER_TEMPLATE = {
    "role": "user",
    "content": (
        "Resume TEXT:\n\n{resume_text}\n\n"
        "Task:\n"
        "1) List mistakes in my resume under a 'Mistakes' heading.\n"
        "2) Add a section for inappropriate or irrelevant items.\n"
        "3) Add a section for what should not be included.\n"
        "4) Add a section for weakening sections.\n"
        "5) Provide 3 short, high-impact improvements (structure, keywords, metrics).\n"
        "6) Provide 3 suggested rewritten bullet points (clearly show BEFORE and AFTER).\n"
        "7) Add an estimated ATS score (0-100) and a 1-sentence reason.\n\n"
        "Output format: Use clean markdown headings and subheadings. Avoid raw JSON."
    )
}
