from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
from datetime import datetime

@dataclass
class AnalysisResult:
    """Class to store and extend the VA opportunity analysis results"""
    
    # Original input
    description: str
    
    # Core analysis scores and explanations
    mission_alignment: Dict[str, Any]
    technical_feasibility: Dict[str, Any]
    competitive_advantage: Dict[str, Any]
    financial_viability: Dict[str, Any]
    risk_compliance: Dict[str, Any]
    
    # Token usage statistics
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    # Metadata
    timestamp: datetime
    model_used: str
    
    @classmethod
    def from_analysis(cls, description: str, analysis_result: Dict[str, Any], completion_info: Any) -> "AnalysisResult":
        """Create an AnalysisResult instance from the raw analysis output"""
        # Extract the opportunity data from the wrapper
        opportunity_data = analysis_result["opportunity"]
        
        return cls(
            description=description,
            mission_alignment=opportunity_data["mission_and_strategic_alignment"],
            technical_feasibility=opportunity_data["technical_feasibility"],
            competitive_advantage=opportunity_data["competitive_advantage"], 
            financial_viability=opportunity_data["financial_contractual_viability"],
            risk_compliance=opportunity_data["risk_and_compliance"],
            prompt_tokens=completion_info.usage.prompt_tokens,
            completion_tokens=completion_info.usage.completion_tokens,
            total_tokens=completion_info.usage.total_tokens,
            timestamp=datetime.now(),
            model_used=completion_info.model
        )
    
    @property
    def average_score(self) -> float:
        """Calculate the average score across all dimensions"""
        scores = [
            self.mission_alignment["score"],
            self.technical_feasibility["score"],
            self.competitive_advantage["score"],
            self.financial_viability["score"],
            self.risk_compliance["score"]
        ]
        return sum(scores) / len(scores)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the analysis result to a dictionary"""
        return {
            "description": self.description,
            "scores": {
                "mission_alignment": self.mission_alignment,
                "technical_feasibility": self.technical_feasibility,
                "competitive_advantage": self.competitive_advantage,
                "financial_viability": self.financial_viability,
                "risk_compliance": self.risk_compliance,
                "average_score": self.average_score
            },
            "usage": {
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "total_tokens": self.total_tokens
            },
            "metadata": {
                "timestamp": self.timestamp.isoformat(),
                "model": self.model_used
            }
        }
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Convert the analysis result to a JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
