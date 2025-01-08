import json
import logging
from ..config.config import client
from ..analysis.analysis_results import AnalysisResult
from ..schemas.schema import json_schema

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_use_case(description):
    logging.info("Starting analysis for the provided use case description.")
    try:
        logging.debug(f"Use case description: {description}")
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant evaluating government contract opportunities (particularly for the VA) on behalf of a company specializing in platform and app delivery. "
                        "The company focuses on achieving outcomes in production through rapid, continuous software delivery, emphasizing speed, security, and reliability. "
                        "Their expertise includes:\n"
                        "• Cloud & Platform (microservices, containers, DevSecOps, SRE)\n"
                        "• Applications & Data (AI/ML, data science, application modernization)\n"
                        "• Security & Compliance (NIST RMF, ATO for Continuous Delivery)\n"
                        "• Product & Execution (value stream mapping, outcome-oriented roadmaps)\n"
                        "• Strategy & Operating Model (digital operating model, workforce enablement)\n\n"
                        "They prioritize engagements where they deliver working platforms or applications in production over pure consulting or enablement.\n\n"
                        "Using the JSON schema provided (mission_and_strategic_alignment, technical_feasibility, competitive_advantage, financial_contractual_viability, risk_and_compliance), "
                        "assess each opportunity against the company’s strengths, goals, and risk tolerance. "
                        "Return a valid JSON object that strictly conforms to the schema:\n\n"
                        "1. mission_and_strategic_alignment: numeric score and an explanation of how well the project aligns with their mission to continuously deliver valuable software.\n"
                        "2. technical_feasibility: numeric score and an explanation relating to the company's platform/app delivery skill set.\n"
                        "3. competitive_advantage: numeric score and an explanation referencing how they differentiate from competitors.\n"
                        "4. financial_contractual_viability: numeric score and an explanation of how well the deal structure and revenue potential fit their business model.\n"
                        "5. risk_and_compliance: numeric score and an explanation of how they can meet or exceed compliance and security requirements with minimal risk.\n\n"
                        "Your response must be concise, yet detailed enough to justify each score."
                    )
                },
                {
                    "role": "user",
                    "content": description
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "VAAIProjectAnalysis",
                    "strict": True,
                    "schema": json_schema
                }
            }
        )
        logging.info("Received response from OpenAI API.")
        
        analysis_data = json.loads(completion.choices[0].message.content)
        logging.debug(f"Parsed analysis data: {json.dumps(analysis_data, indent=2)}")
        
        result = AnalysisResult.from_analysis(description, analysis_data, completion)
        
        return result
        
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        logging.error(f"Response content: {completion.choices[0].message.content}")
        raise
