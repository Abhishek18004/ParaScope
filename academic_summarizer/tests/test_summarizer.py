"""
This is a basic unit test that checks if the summarize_text function returns a valid response from 
Gemini using a sample academic paragraph. It verifies both success status and the presence of a 
summary in the output.
"""

import os
import sys

# Dynamically add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.summarizer import summarize_text

def test_summarizer():
    sample = """
    Convolutional Neural Networks (CNNs) are widely used in image recognition tasks.
    They consist of multiple layers of convolutions, pooling, and fully connected layers.
    CNNs leverage spatial hierarchies in data, making them suitable for visual pattern recognition.
    """

    try:
        result = summarize_text(sample, mode="full")

        if not result.get("success"):
            return {
                "success": False,
                "output": result.get("output", "[Error]: Unknown failure from summarizer.")
            }

        if "summary" not in result["output"].lower():
            return {
                "success": False,
                "output": "[Test Error]: Output missing summary section."
            }

        print("✅ Summarization Test Passed")
        return {
            "success": True,
            "output": result["output"]
        }

    except Exception as e:
        print(f"[Test Exception] {e}")
        return {
            "success": False,
            "output": f"[Test Error]: Exception during test run – {str(e)}"
        }

# Run if executed directly
if __name__ == "__main__":
    test_result = test_summarizer()
    print(test_result)
