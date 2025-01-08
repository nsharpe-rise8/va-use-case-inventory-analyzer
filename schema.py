json_schema = {
  "type": "object",
  "properties": {
    "opportunity": {
      "type": "object",
      "properties": {
        "mission_and_strategic_alignment": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Numerical rating of how well this opportunity aligns with core competencies and mission."
            },
            "explanation": {
              "type": "string",
              "description": "Explanation of how this aligns (or does not align) with your strategic goals and mission."
            }
          },
          "required": ["score", "explanation"],
          "additionalProperties": False
        },
        "technical_feasibility": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Numerical rating of the opportunity’s technical fit (technology stack, complexity, timeline feasibility)."
            },
            "explanation": {
              "type": "string",
              "description": "Rationale for how your platform/app delivery capabilities match the technical demands."
            }
          },
          "required": ["score", "explanation"],
          "additionalProperties": False
        },
        "competitive_advantage": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Numerical rating of how strongly you can differentiate against competitors (past performance, unique strengths)."
            },
            "explanation": {
              "type": "string",
              "description": "Justification for why you have a strong (or weak) position versus likely competitors."
            }
          },
          "required": ["score", "explanation"],
          "additionalProperties": False
        },
        "financial_contractual_viability": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Numerical rating of expected financial return and favorable contract terms."
            },
            "explanation": {
              "type": "string",
              "description": "Details on contract structure, revenue potential, and how it fits your business model."
            }
          },
          "required": ["score", "explanation"],
          "additionalProperties": False
        },
        "risk_and_compliance": {
          "type": "object",
          "properties": {
            "score": {
              "type": "number",
              "description": "Numerical rating of perceived risk, compliance demands (CD-RMF, NIST, etc.), and your ability to mitigate."
            },
            "explanation": {
              "type": "string",
              "description": "Explanation of how you’ll address security, compliance, and overall risk exposure."
            }
          },
          "required": ["score", "explanation"],
          "additionalProperties": False
        }
      },
      "required": [
        "mission_and_strategic_alignment",
        "technical_feasibility",
        "competitive_advantage",
        "financial_contractual_viability",
        "risk_and_compliance"
      ],
      "additionalProperties": False
    }
  },
  "required": ["opportunity"],
  "additionalProperties": False
}
