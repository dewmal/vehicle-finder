from groq import Groq

def build_result(query:str,search_results):
  client = Groq()
  
  user_content  = f"""
  ### QUERY
{query}

### RESULTS_JSON
{search_results}
  """
  
  completion = client.chat.completions.create(
      model="openai/gpt-oss-20b",
      messages=[
        {
          "role": "system",
          "content": "You are a concise vehicle Expert assistant.\nYou receive:\n\nA user query describing exactly what they want.\n\nA JSON array of search results (items may include: title, link, image, mileage, location_category, price, updated, and possibly others).\n\nGoals\n\nAnswer the user’s query using only the provided results.\n\nBe short, natural, and conversational, not robotic.\n\nIf needed, compare a few relevant options and make a clear recommendation.\n\nRules\n\nPrioritize relevance to the query (category, budget, location, recency, mileage, features in the title).\n\nPrefer newer/“updated just now/minutes” items when choices are close.\n\nNormalize odd/missing fields gracefully (e.g., empty mileage → skip it).\n\nNo raw JSON in the output; don’t show links unless explicitly asked.\n\nIf nothing matches, say so briefly and offer the closest alternatives from the list (and why).\n\nKeep tone friendly and helpful; 1–2 short paragraphs + up to 3 bullets max if needed.\n\nOutput Style\n\nStart with a one-sentence takeaway.\n\nThen give 1–3 top matches with natural explanations (price, location, mileage if useful, and recency).\n\nEnd with a simple next step (“If you want, I can narrow by X/Y.”)"
        },
        {
          "role": "user",
          "content": user_content
        }
      ],
      temperature=1,
      max_completion_tokens=8192,
      top_p=1,
      reasoning_effort="medium",
      stream=True,
      stop=None
  )

  result = ""
  for chunk in completion:
      if chunk.choices[0].delta.content:
          result += chunk.choices[0].delta.content
  return result


if __name__ == "__main__":
    from query_analyser import analyse_query
    from vehicle_finder_ikman import get_vehicle_details
    query = "I want to buy a vehicle my budget is under 20 million. My plan is use this for daily travel to my office. I have to travel 10 km up and down"    
    results = analyse_query(query)
    ads_list = []
    for r in results:
      ads_list += get_vehicle_details(r)
    
    response = build_result(query,ads_list)
    print(response)

