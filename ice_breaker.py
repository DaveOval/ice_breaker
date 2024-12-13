from typing import Tuple

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookuo_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    likedin_username = linkedin_lookup_agent(name = name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=likedin_username, mock=True)

    twitter_username = twitter_lookup_agent(name = name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
            given the Linkedin information {information},
            and their latest twitter posts {twitter_posts} I want you to create:
            1. a short summary
            2. two interesting facts about them 
            
            Use both information from twitter and linkedin.
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # chain = summary_prompt_template | llm

    chain = summary_prompt_template | llm | summary_parser

    res:Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts" : tweets })

    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Icre Breaker Enter")
    ice_break_with("Eden Marco Udemy")






