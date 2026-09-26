import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool

from tavily_tool import tavily_search


load_dotenv()


# ==================================================
# GROQ MODEL
# ==================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ==================================================
# DESTINATION AGENT
# ==================================================

destination_agent = create_agent(
    model=llm,
    system_prompt="""
You are a destination research agent.

Research the destination using the information
provided to you.

Find:
- Important places to visit
- Activities related to the user's interests
- Wildlife or nature places if relevant
- Useful travel information

Use only the research information provided.

Do not create the complete itinerary.

Give short bullet points.
"""
)


# ==================================================
# BUDGET AGENT
# ==================================================

budget_agent = create_agent(
    model=llm,
    system_prompt="""
You are a travel budget agent.

Estimate the total trip cost using the information
provided to you.

Consider:
- Travel from starting location
- Accommodation
- Food
- Local transportation
- Activities
- Return travel

Use the research information provided.

Give a simple budget breakdown.

Do not create the complete itinerary.
"""
)


# ==================================================
# ITINERARY AGENT
# ==================================================

itinerary_agent = create_agent(
    model=llm,
    system_prompt="""
You are an itinerary planning agent.

Create a practical day-by-day itinerary.

Consider:
- Starting location
- Destination
- Number of days
- User interests
- Places suggested by destination research
- Budget information

Keep travel time realistic.

Use simple bullet points.

Do not add unnecessary explanations.
"""
)


# ==================================================
# FINAL AGENT
# ==================================================

final_agent = create_agent(
    model=llm,
    system_prompt="""
You are the final travel planning agent.

Create the final travel plan using all the
information provided.

Include:
- Starting location
- Destination
- Travel overview
- Day-by-day itinerary
- Places to visit
- Activities
- Estimated budget
- Return travel
- Travel tips

Keep the response under 500 words.

Use clear headings and bullet points.

Do not mention the agents or the research process.
"""
)


# ==================================================
# DESTINATION RESEARCH TOOL
# ==================================================

@tool
def destination_research(request: str) -> str:
    """Research destination places and activities."""

    search_results = tavily_search(request)

    agent_request = f"""
User travel request:

{request}

Web research results:

{search_results}

Based on this information, provide useful
destination places and activities.
"""

    response = destination_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": agent_request
                }
            ]
        }
    )

    return response["messages"][-1].content


# ==================================================
# BUDGET RESEARCH TOOL
# ==================================================

@tool
def budget_research(request: str) -> str:
    """Research and estimate travel costs."""

    search_results = tavily_search(request)

    agent_request = f"""
User travel request:

{request}

Web research results:

{search_results}

Based on this information, provide a simple
estimated travel budget.
"""

    response = budget_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": agent_request
                }
            ]
        }
    )

    return response["messages"][-1].content


# ==================================================
# ITINERARY TOOL
# ==================================================

@tool
def itinerary_planning(request: str) -> str:
    """Create the day-by-day travel itinerary."""

    response = itinerary_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request
                }
            ]
        }
    )

    return response["messages"][-1].content


# ==================================================
# FINAL PLANNING TOOL
# ==================================================

@tool
def final_planning(request: str) -> str:
    """Create the final complete travel plan."""

    response = final_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request
                }
            ]
        }
    )

    return response["messages"][-1].content


# ==================================================
# SUPERVISOR AGENT
# ==================================================

supervisor_agent = create_agent(
    model=llm,

    tools=[
        destination_research,
        budget_research,
        itinerary_planning,
        final_planning
    ],

    system_prompt="""
You are the supervisor of a travel planning system.

You coordinate the specialized travel agents.

Follow this exact process:

1. Call destination_research.

2. Call budget_research.

3. Use the destination research and budget research
   to call itinerary_planning.

4. Use all the information to call final_planning.

5. Return the result from final_planning.

Always use the specialized agents.

Do not create the travel plan yourself.

Pass the useful information from one agent to
the next agent.

The final answer must come from final_planning.
"""
)


# ==================================================
# USER INPUT
# ==================================================

current_location = input(
    "Enter your starting location: "
)

destination = input(
    "Enter destination: "
)

days = input(
    "Enter number of days: "
)

budget = input(
    "Enter your budget: "
)

interests = input(
    "Enter your interests: "
)


# ==================================================
# USER REQUEST
# ==================================================

user_request = f"""
Create a complete travel plan.

Starting location:
{current_location}

Destination:
{destination}

Number of days:
{days}

Budget:
{budget}

Interests:
{interests}
"""


# ==================================================
# RUN SUPERVISOR
# ==================================================

print("\nStarting travel planning...\n")

supervisor_response = supervisor_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": user_request
            }
        ]
    }
)


# ==================================================
# GET FINAL RESULT
# ==================================================

final_text = ""

for message in reversed(
    supervisor_response["messages"]
):

    content = message.content

    if isinstance(content, str):

        if content.strip():

            final_text = content
            break

    elif isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

        if text_parts:

            final_text = "\n".join(
                text_parts
            )

            if final_text.strip():

                break


# ==================================================
# DISPLAY TRAVEL PLAN
# ==================================================

print("\n")
print("----- TRAVEL PLAN -----")
print("\n")

print(final_text)


# ==================================================
# CREATE PDF
# ==================================================

create_pdf = input(
    "\nCreate a PDF of this travel plan? (y/n): "
)

if create_pdf.lower() == "y":

    from pdf_creator import create_pdf

    pdf_file = create_pdf(
        current_location,
        destination,
        days,
        budget,
        interests,
        final_text
    )

    print("\nPDF created successfully:")
    print(pdf_file)