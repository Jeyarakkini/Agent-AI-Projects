## Project Overview

A multi-agent AI travel planning system built with **LangChain, Groq, Tavily, and Python**.

The system takes the user's starting location, destination, number of days, budget, and interests, then uses specialized agents to research the destination, estimate costs, create a day-by-day itinerary, and generate a final travel plan.

### Agents

* **Supervisor Agent** – Coordinates the complete workflow.
* **Destination Agent** – Researches places, activities, and useful travel information.
* **Budget Agent** – Estimates travel, accommodation, food, transport, and activity costs.
* **Itinerary Agent** – Creates a practical day-by-day itinerary.
* **Final Planning Agent** – Combines all information into the final travel plan.

### Tools

* **Tavily Search** – Web research for destination and budget information.
* **LangChain Tools** – Connect the supervisor with the specialized agents.
* **PDF Generator** – Converts the final travel plan into a PDF.

### Workflow

**User Input → Supervisor Agent → Destination Research → Budget Research → Itinerary Planning → Final Planning → Travel Plan → PDF**

### Technologies

**Python | LangChain | Groq | GPT-OSS 120B | Tavily | ReportLab**
