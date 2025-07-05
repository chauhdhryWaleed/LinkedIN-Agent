# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import json
# from typing import Dict, List, TypedDict
# from langchain_groq import ChatGroq
# from langgraph.graph import Graph, StateGraph, END
# from langgraph.prebuilt import ToolInvocation
# import re
# import time
# from dataclasses import dataclass
# from enum import Enum
# from dotenv import load_dotenv
# import os

# # Configuration
# st.set_page_config(
#     page_title="LinkedIn Comment AI Agent",
#     page_icon="💼",
#     layout="wide"
# )

# class CommentType(Enum):
#     QUESTION = "question"
#     OPINION = "opinion"
#     APPRECIATION = "appreciation"

# @dataclass
# class Comment:
#     text: str
#     type: CommentType


# class AgentState(TypedDict):
#     linkedin_url: str
#     post_content: str
#     post_author: str
#     comment_type: CommentType
#     generated_comments: List[Comment]
#     selected_comment: str
#     error: str

# class LinkedInCommentAgent:
#     def __init__(self, groq_api_key: str):
#         self.llm = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama-3.3-70b-versatile",
#             temperature=0.7
#         )
#         self.graph = self._build_graph()
    
#     def _build_graph(self) -> StateGraph:
#         # Define the workflow graph
#         workflow = StateGraph(AgentState)
        
#         # Add nodes
#         workflow.add_node("scrape_post", self.scrape_linkedin_post)
#         workflow.add_node("analyze_post", self.analyze_post)
#         workflow.add_node("generate_comments", self.generate_comments)
#         workflow.add_node("format_output", self.format_output)
        
#         # Add edges
#         workflow.add_edge("scrape_post", "analyze_post")
#         workflow.add_edge("analyze_post", "generate_comments")
#         workflow.add_edge("generate_comments", "format_output")
#         workflow.add_edge("format_output", END)
        
#         # Set entry point
#         workflow.set_entry_point("scrape_post")
        
#         return workflow.compile()
    
#     def scrape_linkedin_post(self, state: AgentState) -> AgentState:
#         """Scrape LinkedIn post content"""
#         try:
#             url = state["linkedin_url"]
            
#             # Headers to mimic a real browser
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.5',
#                 'Accept-Encoding': 'gzip, deflate',
#                 'Connection': 'keep-alive',
#                 'Upgrade-Insecure-Requests': '1',
#             }
            
#             response = requests.get(url, headers=headers, timeout=10)
#             response.raise_for_status()
            
#             # print("in linkedin scraper functioin")
#             # print(response.content)
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             # Extract post content (this is a simplified approach)
#             # In reality, LinkedIn has complex anti-scraping measures
#             post_text = ""
#             author = "Unknown"
            
#             # Try to find post content in various possible containers
#             content_selectors = [
#                 '.feed-shared-update-v2__description',
#                 '.feed-shared-text',
#                 '.attributed-text-segment-list__content',
#                 'span[dir="ltr"]'
#             ]
            
#             for selector in content_selectors:
#                 elements = soup.select(selector)
#                 if elements:
#                     post_text = ' '.join([elem.get_text().strip() for elem in elements])
#                     break
            
#             # Try to find author name
#             author_selectors = [
#                 '.feed-shared-actor__name',
#                 '.feed-shared-actor__title',
#                 'span.visually-hidden'
#             ]
            
#             for selector in author_selectors:
#                 elements = soup.select(selector)
#                 if elements:
#                     author = elements[0].get_text().strip()
#                     break
            
#             if not post_text:
#                 # Fallback: extract all visible text and clean it
#                 post_text = soup.get_text()
#                 post_text = re.sub(r'\s+', ' ', post_text).strip()
#                 post_text = post_text[:1000]  # Limit length
            
#             state["post_content"] = post_text
#             state["post_author"] = author
#             state["error"] = ""
            
#         except Exception as e:
#             state["error"] = f"Error scraping LinkedIn post: {str(e)}"
#             state["post_content"] = ""
#             state["post_author"] = ""
        
#         return state
    
#     def analyze_post(self, state: AgentState) -> AgentState:
#         """Analyze the post content to understand context"""
#         try:
#             if state["error"]:
#                 return state
                
#             post_content = state["post_content"]
            
#             analysis_prompt = f"""
#             Analyze this LinkedIn post and provide insights:
            
#             Post Content: {post_content}
            
#             Please identify:
#             1. Main topic/theme
#             2. Tone (professional, casual, inspirational, etc.)
#             3. Key points made
#             4. Industry/domain context
#             5. Engagement opportunities
            
#             Keep the analysis concise and focused on what would help generate relevant comments.
#             """
            
#             response = self.llm.invoke(analysis_prompt)
#             state["post_analysis"] = response.content
            
#         except Exception as e:
#             state["error"] = f"Error analyzing post: {str(e)}"
        
#         return state
    
#     def generate_comments(self, state: AgentState) -> AgentState:
#         """Generate different types of comments"""
#         try:
#             if state["error"]:
#                 return state
                
#             post_content = state["post_content"]
#             comment_type = state["comment_type"]


#             print("comment type is ",comment_type)

         
            
#             # Generate 3 different comments based on type
#             comments = []
#             prompt=""


            
#             for i in range(3):
#                 print(type(comment_type))
#                 print(type(CommentType.QUESTION))
#                 if comment_type == CommentType.QUESTION:

#                     print("inside the prompt of question type ")
#                     prompt = f"""
#                     Based on this LinkedIn post, generate a thoughtful question that would encourage meaningful discussion:
                    
#                     Post: {post_content}
                    
#                     Generate a professional question that:
#                     - Shows genuine interest in the topic
#                     - Encourages the author to elaborate
#                     - Adds value to the conversation
#                     - Is specific and relevant
                    
#                     Keep it concise (1-2 sentences max).
#                     """
                
#                 elif comment_type == CommentType.OPINION:
#                     prompt = f"""
#                     Based on this LinkedIn post, generate a thoughtful opinion/perspective comment:
                    
#                     Post: {post_content}
                    
#                     Generate a professional comment that:
#                     - Shares a relevant perspective or insight
#                     - Builds on the author's points
#                     - Adds value to the discussion
#                     - Shows expertise or experience
                    
#                     Keep it concise (2-3 sentences max).
#                     """
                
#                 elif comment_type==CommentType.APPRECIATION:  # APPRECIATION
#                     prompt = f"""
#                     Based on this LinkedIn post, generate an appreciative comment:
                    
#                     Post: {post_content}
                    
#                     Generate a professional comment that:
#                     - Shows genuine appreciation for the content
#                     - Highlights specific valuable points
#                     - Encourages the author
#                     - Feels authentic, not generic
                    
#                     Keep it concise (1-2 sentences max).
#                     """
                
#                 print("prompt is ",prompt)
#                 response = self.llm.invoke(prompt)
#                 comment_text = response.content.strip()
                
#                 # Remove quotes if they exist
#                 comment_text = comment_text.strip('"\'')
                
#                 comments.append(Comment(
#                     text=comment_text,
#                     type=comment_type,
                
#                 ))
            
#             state["generated_comments"] = comments
            
#         except Exception as e:
#             state["error"] = f"Error generating comments: {str(e)}"
        
#         return state
    
#     def format_output(self, state: AgentState) -> AgentState:
#         """Format the final output"""
#         return state
    
#     def run(self, linkedin_url: str, comment_type: CommentType) -> AgentState:
#         """Run the complete workflow"""
#         initial_state = {
#             "linkedin_url": linkedin_url,
#             "post_content": "",
#             "post_author": "",
#             "comment_type": comment_type,
#             "generated_comments": [],
#             "selected_comment": "",
#             "error": ""
#         }
        
#         result = self.graph.invoke(initial_state)
#         return result

# def main():
#     st.title("🤖 LinkedIn Comment AI Agent")
#     st.markdown("Generate intelligent comments for LinkedIn posts using AI")
    
#     # Sidebar for configuration
#     with st.sidebar:
#         st.header("⚙️ Configuration")

#         # Load environment variables from .env file
#         load_dotenv()

#         # Get the value of SECRET_KEY
#         groq_api_key = os.getenv("SECRET_KEY")

#         if not groq_api_key:
#             st.warning("Please enter your Groq API key to continue")
#             st.stop()
    
#     # Initialize agent
#     if 'agent' not in st.session_state:
#         st.session_state.agent = LinkedInCommentAgent(groq_api_key)
    
#     # Main interface
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.header("📝 Post Analysis")
#         linkedin_url = st.text_input(
#             "LinkedIn Post URL",
#             placeholder="https://www.linkedin.com/posts/...",
#             help="Paste the LinkedIn post URL you want to comment on"
#         )
        
#         comment_type = st.selectbox(
#             "Comment Type",
#             options=[CommentType.QUESTION, CommentType.OPINION, CommentType.APPRECIATION],
#             format_func=lambda x: {
#                 CommentType.QUESTION: "❓ Question",
#                 CommentType.OPINION: "💭 Opinion/View",
#                 CommentType.APPRECIATION: "👏 Appreciation"
#             }[x]
#         )
    
#     with col2:
#         st.header("🎯 Quick Actions")
#         analyze_button = st.button("🔍 Analyze & Generate", type="primary")
        
#         if st.button("🔄 Generate More Options"):
#             if 'current_state' in st.session_state:
#                 st.session_state.current_state = st.session_state.agent.run(
#                     linkedin_url, comment_type
#                 )
    
#     # Process when button is clicked
#     if analyze_button and linkedin_url:
#         with st.spinner("Analyzing LinkedIn post and generating comments..."):
#             result = st.session_state.agent.run(linkedin_url, comment_type)
#             st.session_state.current_state = result
    
#     # Display results
#     if 'current_state' in st.session_state:
#         state = st.session_state.current_state
        
#         if state.get("error"):
#             st.error(f"Error: {state['error']}")
#         else:
#             # Display post content
#             if state.get("post_content"):
#                 st.header("📄 Post Content")
#                 with st.expander("View Original Post", expanded=False):
#                     st.write(f"**Author:** {state.get('post_author', 'Unknown')}")
#                     st.write(state["post_content"][:500] + "..." if len(state["post_content"]) > 500 else state["post_content"])
            
#             # Display generated comments
#             if state.get("generated_comments"):
#                 st.header("💬 Generated Comments")
                
#                 for i, comment in enumerate(state["generated_comments"], 1):
#                     with st.container():
#                         st.subheader(f"Option {i}")
#                         st.write(comment.text)
                        
#                         col1, col2, col3 = st.columns([1, 1, 2])
                        
#                         with col1:
#                             if st.button(f"✅ Select", key=f"select_{i}"):
#                                 st.session_state.selected_comment = comment.text
#                                 st.success("Comment selected!")
                        
#                         with col2:
#                             if st.button(f"📝 Edit", key=f"edit_{i}"):
#                                 st.session_state.edit_comment = comment.text
                        
                        
#                         st.divider()
                
#                 # Show selected comment
#                 if 'selected_comment' in st.session_state:
#                     st.header("🎯 Selected Comment")
#                     st.info(st.session_state.selected_comment)
                    
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         st.button("📋 Copy to Clipboard", help="Copy comment to clipboard")
#                     with col2:
#                         st.button("🚀 Post to LinkedIn", help="This would integrate with LinkedIn API")
                
#                 # Edit comment section
#                 if 'edit_comment' in st.session_state:
#                     st.header("✏️ Edit Comment")
#                     edited_comment = st.text_area(
#                         "Edit your comment:",
#                         value=st.session_state.edit_comment,
#                         height=100
#                     )
                    
#                     if st.button("💾 Save Changes"):
#                         st.session_state.selected_comment = edited_comment
#                         del st.session_state.edit_comment
#                         st.success("Comment updated!")
#                         st.rerun()
    
#     # Footer
#     st.markdown("---")
#     st.markdown("*Note: This tool generates comments based on publicly available post content. Always review and personalize comments before posting.*")

# if __name__ == "__main__":
#     main()




import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import Graph, StateGraph, END
from langgraph.prebuilt import ToolInvocation
import re
import time
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
import os


# Configuration
st.set_page_config(
    page_title="LinkedIn Comment AI Agent",
    page_icon="💼",
    layout="wide"
)

class CommentType(Enum):
    QUESTION = "question"
    OPINION = "opinion"
    APPRECIATION = "appreciation"

@dataclass
class Comment:
    text: str
    type: CommentType


class AgentState(TypedDict):
    linkedin_url: str
    post_content: str
    post_author: str
    comment_type: CommentType
    generated_comments: List[Comment]
    selected_comment: str
    error: str

class LinkedInCommentAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.7
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        # Define the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("scrape_post", self.scrape_linkedin_post)
        workflow.add_node("analyze_post", self.analyze_post)
        workflow.add_node("generate_comments", self.generate_comments)
        workflow.add_node("format_output", self.format_output)
        
        # Add edges
        workflow.add_edge("scrape_post", "analyze_post")
        workflow.add_edge("analyze_post", "generate_comments")
        workflow.add_edge("generate_comments", "format_output")
        workflow.add_edge("format_output", END)
        
        # Set entry point
        workflow.set_entry_point("scrape_post")
        
        return workflow.compile()
    
    def scrape_linkedin_post(self, state: AgentState) -> AgentState:
        """Scrape LinkedIn post content"""
        try:
            url = state["linkedin_url"]
            
            # Headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract post content (this is a simplified approach)
            # In reality, LinkedIn has complex anti-scraping measures
            post_text = ""
            author = "Unknown"
            
            # Try to find post content in various possible containers
            content_selectors = [
                '.feed-shared-update-v2__description',
                '.feed-shared-text',
                '.attributed-text-segment-list__content',
                'span[dir="ltr"]'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    post_text = ' '.join([elem.get_text().strip() for elem in elements])
                    break
            
            # Try to find author name
            author_selectors = [
                '.feed-shared-actor__name',
                '.feed-shared-actor__title',
                'span.visually-hidden'
            ]
            
            for selector in author_selectors:
                elements = soup.select(selector)
                if elements:
                    author = elements[0].get_text().strip()
                    break
            
            if not post_text:
                # Fallback: extract all visible text and clean it
                post_text = soup.get_text()
                post_text = re.sub(r'\s+', ' ', post_text).strip()
                post_text = post_text[:1000]  # Limit length
            
            state["post_content"] = post_text
            state["post_author"] = author
            state["error"] = ""
            
        except Exception as e:
            state["error"] = f"Error scraping LinkedIn post: {str(e)}"
            state["post_content"] = ""
            state["post_author"] = ""
        
        return state
    
    def analyze_post(self, state: AgentState) -> AgentState:
        """Analyze the post content to understand context"""
        try:
            if state["error"]:
                return state
                
            post_content = state["post_content"]
            
            analysis_prompt = f"""
            Analyze this LinkedIn post and provide insights:
            
            Post Content: {post_content}
            
            Please identify:
            1. Main topic/theme
            2. Tone (professional, casual, inspirational, etc.)
            3. Key points made
            4. Industry/domain context
            5. Engagement opportunities
            
            Keep the analysis concise and focused on what would help generate relevant comments.
            """
            
            response = self.llm.invoke(analysis_prompt)
            state["post_analysis"] = response.content
            
        except Exception as e:
            state["error"] = f"Error analyzing post: {str(e)}"
        
        return state
    
    def generate_comments(self, state: AgentState) -> AgentState:
        """Generate different types of comments"""
        try:
            if state["error"]:
                return state
                
            post_content = state["post_content"]
            comment_type = state["comment_type"]
            
            print("comment type is:", comment_type)
            print("comment type value:", comment_type.value)
            
            # Generate 3 different comments based on type
            comments = []
            
            for i in range(3):
                prompt = ""  # Initialize prompt
                
                if comment_type.value == "question":
                    print("inside the prompt of question type")
                    prompt = f"""
                    Based on this LinkedIn post, generate a thoughtful question that would encourage meaningful discussion:
                    
                    Post: {post_content}
                    
                    Generate a professional question that:
                    - Shows genuine interest in the topic
                    - Encourages the author to elaborate
                    - Adds value to the conversation
                    - Is specific and relevant
                    
                    Keep it concise (1-2 sentences max).
                    """
                
                elif comment_type.value == "opinion":
                    print("inside the prompt of opinion type")
                    prompt = f"""
                    Based on this LinkedIn post, generate a thoughtful opinion/perspective comment:
                    
                    Post: {post_content}
                    
                    Generate a professional comment that:
                    - Shares a relevant perspective or insight
                    - Builds on the author's points
                    - Adds value to the discussion
                    - Shows expertise or experience
                    
                    Keep it concise (2-3 sentences max).
                    """
                
                elif comment_type.value == "appreciation":
                    print("inside the prompt of appreciation type")
                    prompt = f"""
                    Based on this LinkedIn post, generate an appreciative comment:
                    
                    Post: {post_content}
                    
                    Generate a professional comment that:
                    - Shows genuine appreciation for the content
                    - Highlights specific valuable points
                    - Encourages the author
                    - Feels authentic, not generic
                    
                    Keep it concise (1-2 sentences max).
                    """
                
                print("prompt is:", prompt[:100], "...")  # Print first 100 chars
                
                if prompt:  # Only invoke if prompt is not empty
                    response = self.llm.invoke(prompt)
                    comment_text = response.content.strip()
                    
                    # Remove quotes if they exist
                    comment_text = comment_text.strip('"\'')
                    
                    comments.append(Comment(
                        text=comment_text,
                        type=comment_type
                    ))
                else:
                    print("Warning: Empty prompt generated")
            
            state["generated_comments"] = comments
            
        except Exception as e:
            state["error"] = f"Error generating comments: {str(e)}"
            print("Error in generate_comments:", str(e))
        
        return state
    
    def format_output(self, state: AgentState) -> AgentState:
        """Format the final output"""
        return state
    
    def run(self, linkedin_url: str, comment_type: CommentType) -> AgentState:
        """Run the complete workflow"""
        initial_state = {
            "linkedin_url": linkedin_url,
            "post_content": "",
            "post_author": "",
            "comment_type": comment_type,
            "generated_comments": [],
            "selected_comment": "",
            "error": ""
        }
        
        result = self.graph.invoke(initial_state)
        return result

def main():
    st.title("🤖 LinkedIn Comment AI Agent")
    st.markdown("Generate intelligent comments for LinkedIn posts using AI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        # Load environment variables from .env file
        load_dotenv()

        # Get the value of SECRET_KEY
        groq_api_key = os.getenv("SECRET_KEY")

        if not groq_api_key:
            st.warning("Please enter your Groq API key to continue")
            st.stop()
    
    # Initialize agent
    if 'agent' not in st.session_state:
        st.session_state.agent = LinkedInCommentAgent(groq_api_key)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Post Analysis")
        linkedin_url = st.text_input(
            "LinkedIn Post URL",
            placeholder="https://www.linkedin.com/posts/...",
            help="Paste the LinkedIn post URL you want to comment on"
        )
        
        comment_type = st.selectbox(
            "Comment Type",
            options=[CommentType.QUESTION, CommentType.OPINION, CommentType.APPRECIATION],
            format_func=lambda x: {
                CommentType.QUESTION: "❓ Question",
                CommentType.OPINION: "💭 Opinion/View",
                CommentType.APPRECIATION: "👏 Appreciation"
            }[x]
        )
    
    with col2:
        st.header("🎯 Quick Actions")
        analyze_button = st.button("🔍 Analyze & Generate", type="primary")
        
        if st.button("🔄 Generate More Options"):
            if 'current_state' in st.session_state:
                st.session_state.current_state = st.session_state.agent.run(
                    linkedin_url, comment_type
                )
    
    # Process when button is clicked
    if analyze_button and linkedin_url:
        with st.spinner("Analyzing LinkedIn post and generating comments..."):
            result = st.session_state.agent.run(linkedin_url, comment_type)
            st.session_state.current_state = result
    
    # Display results
    if 'current_state' in st.session_state:
        state = st.session_state.current_state
        
        if state.get("error"):
            st.error(f"Error: {state['error']}")
        else:
            # Display post content
            if state.get("post_content"):
                st.header("📄 Post Content")
                with st.expander("View Original Post", expanded=False):
                    st.write(f"**Author:** {state.get('post_author', 'Unknown')}")
                    st.write(state["post_content"][:500] + "..." if len(state["post_content"]) > 500 else state["post_content"])
            
            # Display generated comments
            if state.get("generated_comments"):
                st.header("💬 Generated Comments")
                
                for i, comment in enumerate(state["generated_comments"], 1):
                    with st.container():
                        st.subheader(f"Option {i}")
                        st.write(comment.text)
                        
                        col1, col2, col3 = st.columns([1, 1, 2])
                        
                        with col1:
                            if st.button(f"✅ Select", key=f"select_{i}"):
                                st.session_state.selected_comment = comment.text
                                st.success("Comment selected!")
                        
                        with col2:
                            if st.button(f"📝 Edit", key=f"edit_{i}"):
                                st.session_state.edit_comment = comment.text
                        
               
               
                        
                        st.divider()
                
                # Show selected comment
                if 'selected_comment' in st.session_state:
                    st.header("🎯 Selected Comment")
                    st.info(st.session_state.selected_comment)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("📋 Copy to Clipboard", help="Copy comment to clipboard")
                    with col2:
                        st.button("🚀 Post to LinkedIn", help="This would integrate with LinkedIn API")
                
                # Edit comment section
                if 'edit_comment' in st.session_state:
                    st.header("✏️ Edit Comment")
                    edited_comment = st.text_area(
                        "Edit your comment:",
                        value=st.session_state.edit_comment,
                        height=100
                    )
                    
                    if st.button("💾 Save Changes"):
                        st.session_state.selected_comment = edited_comment
                        del st.session_state.edit_comment
                        st.success("Comment updated!")
                        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("*Note: This tool generates comments based on publicly available post content. Always review and personalize comments before posting.*")

if __name__ == "__main__":
    main()