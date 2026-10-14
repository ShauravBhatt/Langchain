from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
  Artificial intelligence (AI) is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making.

  It is a field of research in engineering, mathematics, and computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximise their chances of achieving defined goals.

  High-profile applications of AI include advanced web search engines, chatbots, virtual assistants, autonomous vehicles, play and analysis in strategy games (e.g., chess and Go), and content generation (e.g., text, images, audio, and video.
"""

splitter = RecursiveCharacterTextSplitter(
  chunk_size = 350,
  chunk_overlap = 0,
  separators=["\n\n", "\n", " ", ""]
)

result = splitter.split_text(text)

print(result) 