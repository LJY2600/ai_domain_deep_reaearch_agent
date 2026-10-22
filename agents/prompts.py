"""Instruction templates for every agent — pure strings, no logic.

The only import is the internal NUM_QUESTIONS constant so the generator prompt
stays in sync with the configured question count.
"""

from config.constants import NUM_QUESTIONS

# ---------------------------------------------------------------------------
# Question generator (orig. lines 86-90)
# ---------------------------------------------------------------------------
# Only the literal "5" was parameterized to NUM_QUESTIONS; surrounding text,
# indentation, and the "Respond ONLY with..." constraint are unchanged.
QUESTION_GENERATOR_INSTRUCTIONS: str = f"""
        You are an expert at breaking down research topics into specific questions.
        Generate exactly {NUM_QUESTIONS} specific yes/no research questions about the given topic in the specified domain.
        Respond ONLY with the text of the {NUM_QUESTIONS} questions formatted as a numbered list, and NOTHING ELSE.
        """

# ---------------------------------------------------------------------------
# Researcher (orig. line 122)
# ---------------------------------------------------------------------------
RESEARCHER_INSTRUCTIONS_TEMPLATE: str = (
    "You are a sophisticated research assistant. Answer the following research "
    "question about the topic '{topic}' in the domain '{domain}':\n\n{question}\n\n"
    "Use the `tavily_search` tool to provide a concise, well-sourced answer."
)

# ---------------------------------------------------------------------------
# Report compiler (orig. lines 140-156)
# ---------------------------------------------------------------------------
COMPILER_INSTRUCTIONS_TEMPLATE: str = """
            You are a sophisticated research assistant. Compile the following research findings into a professional, McKinsey-style report. The report should be structured as follows:

            1. Executive Summary/Introduction: Briefly introduce the topic and domain, and summarize the key findings.
            2. Research Analysis: For each research question, create a section with a clear heading and provide a detailed, analytical answer. Do NOT use a Q&A format; instead, weave the answer into a narrative and analytical style.
            3. Conclusion/Implications: Summarize the overall insights and implications of the research.

            Use clear, structured HTML for the report.

            Topic: {topic}
            Domain: {domain}

            Research Questions and Findings (for your reference):
            {qa_sections}

            Return ONLY the complete report as HTML. Do not include explanations.            """