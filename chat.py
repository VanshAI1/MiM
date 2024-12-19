import streamlit as st
from groq import Groq
import json
import uuid
import os
class EssayTherapyCompanion:
    def __init__(self):
        self.groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        self._initialize_conversation_state()

    def _initialize_conversation_state(self):
        """Initialize a gentle, progressive conversation state."""
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = str(uuid.uuid4())
        
        # Minimal, incremental state tracking
        state_keys = {
            'current_phase': 'initial_exploration',
            'responses': {},
            'explored_depths': [],
            'essay_draft': None
        }
        
        for key, default_value in state_keys.items():
            if key not in st.session_state:
                setattr(st.session_state, key, default_value)

    def _generate_compassionate_question(self, context=None):
        """
        Generate a soft, probing question that feels 
        more like a gentle conversation than an interrogation. And start with small questions then go deep.
        """
        system_prompt = """
        You are a compassionate career counselor and narrative guide. 
        Your goal is to ask a single, delicate question that:
        - Feels warm and non-threatening
        - Invites genuine, vulnerable reflection
        - Uncovers hidden personal narratives
        - Creates a safe emotional space for exploration

        Questioning Principles:
        1. Questions should be:
           - Conversational in tone
           - Open-ended but focused
           - Emotionally intelligent
           - Subtly provocative

        2. Approach:
           - Start with seemingly simple inquiries
           - Allow for organic storytelling
           - Create space for unexpected revelations


        Design a question that feels like a caring friend 
        genuinely interested in understanding someone's journey. Make the questions small that lead to deep understanding of the response.
        """

        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt.format(context=context or "Initial gentle exploration")},
                    {"role": "user", "content": "Craft a question that feels like a warm, curious invitation to share."}
                ],
                max_tokens=300,
                temperature=0.5
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            st.error(f"Question Generation Error: {e}")
            return "What small moment in your life has quietly shaped who you are today?"

    def _analyze_response_depth(self, response):
        """
        Gently extract deeper narrative layers 
        from the candidate's response.
        """
        analysis_prompt = """
        Compassionate Narrative Analysis:
        Please provide your analysis in JSON format with the following structure:
        {
            "emotional_themes": [],
            "unspoken_motivations": [],
            "growth_indicators": [],
            "narrative_threads": []
        }
        
        Softly Decode Response Dimensions:
        1. Emotional Undertones
        2. Unspoken Motivations
        3. Personal Growth Indicators
        4. Potential Narrative Threads

        Analysis Approach:
        - Listen between the lines
        - Identify subtle personal transformations
        - Recognize potential for deeper exploration
        - Respect the vulnerability of sharing

        Provide Gentle Insights:
        - Emerging Personal Themes
        - Potential Narrative Directions
        - Areas of Potential Deeper Reflection
        """

        try:
            analysis_response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": analysis_prompt},
                    {"role": "user", "content": f"Please analyze the following reflection and respond in JSON format:\n{response}"}
                ],
                response_format={"type": "json_object"},
                max_tokens=500,
                temperature=0.6
            )

            return json.loads(analysis_response.choices[0].message.content)

        except Exception as e:
            st.error(f"Response Analysis Error: {e}")
            return {
                "emotional_themes": ["Personal Growth", "Resilience"],
                "unspoken_motivations": ["Self-improvement"],
                "growth_indicators": ["Reflection"],
                "narrative_threads": ["Personal Journey"]
            }

    def _generate_intimate_essay(self, insights):
        """
        Craft a deeply personal, authentic narrative 
        that reveals the candidate's true essence.
        """
        essay_prompt = """
        Narrative Intimacy: Transform Personal Reflections 
        into a Profoundly Authentic Master's Application Essay

        Storytelling Essence:
        - Reveal the soul behind the achievements
        - Connect personal journey to professional aspiration
        - Create an emotionally resonant narrative
        - Demonstrate vulnerability and strength

        Narrative Construction:
        1. Opening: Intimate Personal Revelation
        2. Middle: Bridge Personal Growth to Professional Vision
        3. Conclusion: Illuminate Potential for Transformative Leadership

        Candidate's Intimate Insights: {insights}

        Create an essay that:
        - Feels deeply personal
        - Demonstrates intellectual and emotional depth
        - Shows potential beyond traditional metrics
        - Leaves a lasting emotional impression
        """

        try:
            essay_response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": essay_prompt.format(insights=json.dumps(insights))},
                    {"role": "user", "content": "Weave a narrative that reveals the candidate's true potential."}
                ],
                max_tokens=1500,
                temperature=0.8
            )

            return essay_response.choices[0].message.content.strip()

        except Exception as e:
            st.error(f"Essay Generation Error: {e}")
            return "A personal reflection on growth, potential, and the transformative power of continuous learning."

    def interactive_exploration(self):
        """
        Create a gentle, progressive conversation 
        for narrative discovery.
        """
        st.title("🌱 MiM Essay Personal Journey Companion")
        
        # Initial or continuing question generation
        if st.session_state.current_phase == 'initial_exploration':
            st.session_state.current_question = self._generate_compassionate_question()
        
        st.write(f"💬 {st.session_state.current_question}")
        
        # User response collection
        user_response = st.text_area("Your Reflection:", key="user_input")
        
        if st.button("Continue Exploring"):
            if user_response:
                # Store response
                current_response_key = len(st.session_state.responses)
                st.session_state.responses[current_response_key] = user_response
                
                # Analyze response
                response_analysis = self._analyze_response_depth(user_response)
                
                # Update exploration state
                st.session_state.explored_depths.append(response_analysis)
                
                # Determine next step
                if len(st.session_state.explored_depths) < 5:
                    # Continue exploration
                    st.session_state.current_question = self._generate_compassionate_question(
                        context=json.dumps(response_analysis)
                    )
                else:
                    # Generate essay
                    st.session_state.essay_draft = self._generate_intimate_essay(
                        insights=st.session_state.explored_depths
                    )
                    st.success("Your Personal Narrative Emerges...")
                    st.write(st.session_state.essay_draft)

def main():
    companion = EssayTherapyCompanion()
    companion.interactive_exploration()

if __name__ == "__main__":
    main()