from typing import Dict, Any, Optional, List
from datetime import datetime
import re
import asyncio
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class CostResearchService:
    def __init__(self):
        """Initialize the cost research service with LLM and search tools"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.1
        )
        self.search = DuckDuckGoSearchRun()
        self.tools = [self.search]
        # Using the modern LangGraph prebuilt ReAct agent
        self.agent = create_react_agent(self.llm, tools=self.tools)

    async def _run_agent(self, prompt: str) -> str:
        """Helper to run the LangGraph agent and extract the final response"""
        try:
            result = await self.agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
            # LangGraph ReAct agent returns the full message history in "messages"
            # The last message should be the AI's final response
            content = result["messages"][-1].content
            
            # Handle list content (common in some model/LLM versions)
            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(part["text"])
                    elif isinstance(part, str):
                        text_parts.append(part)
                return "".join(text_parts)
            
            return str(content)
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise

    async def research_tuition_costs(self, city: str, year: str, university_name: Optional[str] = None) -> Dict[str, Any]:
        """Research tuition costs for universities in the specified city"""
        logger.info(f"Starting tuition research for {city}, {year}, university: {university_name}")
        
        try:
            # Define tuition-focused search queries
            if university_name:
                search_queries = [
                    f"{university_name} tuition fees {year} international students",
                    f"{university_name} graduate school tuition {year}",
                    f"{university_name} fees structure {year} F1 visa",
                    f"{university_name} financial aid international students {year}",
                    f"{university_name} total cost attendance {year}"
                ]
            else:
                search_queries = [
                    f"{city} university tuition costs {year} international students",
                    f"{city} graduate school tuition fees {year}",
                    f"{city} universities international student fees {year}",
                    f"{city} higher education costs {year} F1 visa",
                    f"top universities {city} tuition comparison {year}",
                    f"{city} university financial aid international students {year}"
                ]
            
            # Collect search results
            all_results = []
            for query in search_queries:
                try:
                    result = await asyncio.to_thread(self.search.run, query)
                    all_results.append(f"Query: {query}\nResults: {result}\n")
                except Exception as e:
                    logger.error(f"Search failed for {query}: {e}")
            
            # Combine results
            search_data = "\n".join(all_results)
            
            # Create tuition summarization prompt
            university_info = f"at {university_name}" if university_name else f"in {city}"
            
            tuition_prompt = f"""
            Based on the following search results, create a comprehensive tuition cost guide for an international graduate student on F1 visa planning to study {university_info} in {year}.

            Search Results:
            {search_data}

            Provide a comprehensive tuition cost guide for an international graduate student on F1 visa planning to study {university_info} in {year}.

            Please provide:

            1. **Tuition Costs Breakdown**:
            - Graduate program tuition (per semester/year)
            - International student fees
            - Technology/Lab fees
            - Health insurance requirements
            - Other mandatory fees

            2. **University Comparison** (if multiple universities in city):
            - List major universities with tuition ranges
            - Ranking vs cost analysis

            3. **Financial Aid Options**:
            - Scholarships for international students
            - Graduate assistantships (TA/RA opportunities)
            - Work study programs
            - Fellowship opportunities

            4. **Payment Options**:
            - Payment plans available
            - Currency exchange considerations
            - International wire transfer fees

            5. **F1 Visa Financial Requirements**:
            - I-20 tuition amount requirements
            - Proof of funds needed
            - SEVIS fee information

            6. **Money-Saving Strategies**:
            - In-state tuition possibilities
            - Course load optimization
            - Summer session costs

            Format as a clear, practical guide with specific dollar amounts where possible.
            Include estimated total costs for different scenarios (1-year masters, 2-year masters, PhD, etc.).
            """
            
            response = await self._run_agent(tuition_prompt)
            
            return {
                "status": "success",
                "data": response,
                "city": city,
                "year": year,
                "university": university_name,
                "research_type": "tuition"
            }
            
        except Exception as e:
            logger.error(f"Error in tuition research: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "city": city,
                "year": year,
                "university": university_name,
                "research_type": "tuition"
            }

    async def research_cost_of_living(self, city: str, year: str) -> Dict[str, Any]:
        """Research and summarize cost of living for international grad students"""
        logger.info(f"Starting cost of living research for {city}, {year}")
        
        try:
            search_queries = [
                f"{city} cost of living {year} international students",
                f"{city} rent prices {year} graduate students",
                f"{city} food costs {year} grocery prices",
                f"{city} public transportation costs {year} student discounts",
                f"{city} university housing costs {year}",
                f"F1 visa financial requirements {city} {year}"
            ]
            
            # Collect search results
            all_results = []
            for query in search_queries:
                try:
                    result = await asyncio.to_thread(self.search.run, query)
                    all_results.append(f"Query: {query}\nResults: {result}\n")
                except Exception as e:
                    logger.error(f"Search failed for {query}: {e}")
            
            search_data = "\n".join(all_results)
            
            prompt = f"""
            Based on the following search results, create a comprehensive cost of living guide for an international graduate student on F1 visa planning to study in {city} in {year}.

            Search Results:
            {search_data}

            Create a comprehensive cost of living guide for an international graduate student on F1 visa planning to study in {city} in {year}.

            Please provide:

            1. **Monthly Budget Breakdown**:
            - Housing/Rent (include on-campus vs off-campus options)
            - Food (groceries, dining out, meal plans)  
            - Transportation (public transit, student discounts)
            - Utilities & Other (phone, internet, health insurance)
            - Books & Supplies
            - Personal/Entertainment

            2. **Annual Total Estimate**

            3. **F1 Visa Considerations**:
            - I-20 financial requirements
            - Bank statement amounts needed
            - Work restrictions and opportunities

            4. **Money-Saving Tips** for international students

            5. **Housing Recommendations** (best areas, types of accommodation)

            Format as a clear, practical guide with specific dollar amounts and ranges where possible.
            """
            
            response = await self._run_agent(prompt)
            
            return {
                "status": "success",
                "data": response,
                "city": city,
                "year": year,
                "research_type": "cost_of_living"
            }
            
        except Exception as e:
            logger.error(f"Error in cost of living research: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "city": city,
                "year": year,
                "research_type": "cost_of_living"
            }

    async def research_funding_options(self, total_estimated_cost: float, year: str, destination_country: str = "USA") -> Dict[str, Any]:
        """Research funding options from Indian financial institutions"""
        logger.info(f"Starting funding research for ${total_estimated_cost:,.2f} in {destination_country}, {year}")
        
        try:
            search_queries = [
                f"education loan India {year} study abroad interest rates",
                f"SBI HDFC ICICI education loan {year} overseas study",
                f"Indian banks student loan {destination_country} {year} interest rates",
                f"education loan without collateral India {year} {destination_country}",
                f"best education loan India {year} processing fees comparison",
                f"government education loan schemes India {year} study abroad",
                f"NBFC education loans India {year} {destination_country} students",
                f"education loan eligibility criteria India {year} overseas"
            ]
            
            # Collect search results
            all_results = []
            for query in search_queries:
                try:
                    result = await asyncio.to_thread(self.search.run, query)
                    all_results.append(f"Query: {query}\nResults: {result}\n")
                except Exception as e:
                    logger.error(f"Search failed for {query}: {e}")
            
            search_data = "\n".join(all_results)
            
            funding_prompt = f"""
            Based on the following search results, create a comprehensive funding guide for an Indian student planning to study in {destination_country} in {year}.

            ESTIMATED TOTAL COST NEEDED: ${total_estimated_cost:,.2f} (approximately ₹{total_estimated_cost * 86:,.0f})

            Search Results:
            {search_data}

            Create a comprehensive funding guide for an Indian student planning to study in {destination_country} in {year}.

            ESTIMATED TOTAL COST NEEDED: ${total_estimated_cost:,.2f} (approximately ₹{total_estimated_cost * 86:,.0f})

            Search Results:
            {search_data}

            Please provide:

            1. **MAJOR INDIAN BANKS EDUCATION LOANS**:
            - State Bank of India (SBI) - interest rates, loan amount, features
            - HDFC Bank - interest rates, terms, eligibility
            - ICICI Bank - rates, processing fees, special schemes
            - Axis Bank - education loan features and rates
            - Bank of Baroda - overseas education loan details

            2. **LOAN AMOUNT CATEGORIES**:
            - Up to ₹7.5 lakhs (without collateral)
            - ₹7.5 lakhs to ₹1.5 crores (with collateral/co-applicant)
            - Above ₹1.5 crores (premium loan products)

            3. **INTEREST RATES ANALYSIS**:
            - Current interest rate ranges (fixed vs floating)
            - Rate variations based on loan amount
            - Special rates for premier institutions
            - Women applicant benefits/concessions

            4. **LOAN FEATURES COMPARISON**:
            - Processing fees and other charges
            - Moratorium period (study period + 1 year)
            - Repayment tenure options
            - Pre-payment and part-payment options

            5. **ELIGIBILITY & DOCUMENTATION**:
            - Age criteria and academic requirements
            - Co-applicant requirements
            - Collateral requirements for different loan amounts
            - Documents needed for loan application

            6. **GOVERNMENT SCHEMES & SUBSIDIES**:
            - Central Sector Interest Subsidy Scheme
            - Dr. A.P.J. Abdul Kalam Interest Subsidy Scheme
            - State government schemes

            7. **NBFCs & ALTERNATIVE LENDERS**:
            - Credila Financial Services
            - Avanse Financial Services
            - Prodigy Finance

            8. **LOAN RECOMMENDATION**:
            Based on the estimated cost of ${total_estimated_cost:,.2f}:
            - Best 3 loan options with reasons
            - Estimated EMI calculations
            - Total interest outgo over loan tenure
            - Tax benefits available (Section 80E)

            9. **APPLICATION STRATEGY**:
            - Timeline for loan application
            - Tips for faster approval
            - Common rejection reasons to avoid

            Format as a practical, actionable funding guide with current {year} rates and terms.
            """
            
            response = await self._run_agent(funding_prompt)
            
            return {
                "status": "success",
                "data": response,
                "total_cost": total_estimated_cost,
                "year": year,
                "destination_country": destination_country,
                "research_type": "funding"
            }
            
        except Exception as e:
            logger.error(f"Error in funding research: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "total_cost": total_estimated_cost,
                "year": year,
                "destination_country": destination_country,
                "research_type": "funding"
            }

    def extract_cost_estimate(self, tuition_report: str, living_report: str) -> float:
        """Extract estimated total cost from research reports using LLM"""
        try:
            extraction_prompt = f"""
            From the following tuition and cost of living research reports, extract the most likely total annual cost estimate for an international student.

            TUITION REPORT:
            {tuition_report}

            COST OF LIVING REPORT:
            {living_report}

            Please analyze both reports and provide:
            1. Annual tuition cost estimate (in USD)
            2. Annual living cost estimate (in USD)  
            3. Total annual cost (tuition + living)

            Return ONLY the total annual cost as a number (no currency symbol, no commas).
            If multiple scenarios exist, use the middle/realistic estimate.
            Example response: 75000
            """
            
            response = self.llm.invoke([{"role": "user", "content": extraction_prompt}])
            
            # Extract number from response
            numbers = re.findall(r'\d+', response.content.replace(',', ''))
            if numbers:
                return float(numbers[-1])  # Take the last number (likely the total)
            return 70000.0  # Default fallback
            
        except Exception as e:
            logger.error(f"Error extracting cost estimate: {str(e)}")
            return 70000.0  # Default fallback

    async def research_comprehensive_costs(
        self, 
        city: str, 
        year: str, 
        university_name: Optional[str] = None, 
        destination_country: str = "USA"
    ) -> Dict[str, Any]:
        """Research tuition, living costs, funding options, then provide comprehensive summary"""
        logger.info(f"Starting comprehensive cost research for {city}, {destination_country} in {year}")
        
        try:
            # Step 1: Research tuition costs
            tuition_result = await self.research_tuition_costs(city, year, university_name)
            
            # Step 2: Research cost of living  
            living_result = await self.research_cost_of_living(city, year)
            
            # Step 3: Extract cost estimates
            if tuition_result["status"] == "success" and living_result["status"] == "success":
                total_estimated_cost = self.extract_cost_estimate(
                    tuition_result["data"], 
                    living_result["data"]
                )
            else:
                total_estimated_cost = 70000.0  # Default estimate
            
            # Step 4: Research funding options
            funding_result = await self.research_funding_options(
                total_estimated_cost, year, destination_country
            )
            
            # Step 5: Create comprehensive summary
            if all(result["status"] == "success" for result in [tuition_result, living_result, funding_result]):
                final_prompt = f"""
                Create a comprehensive financial planning guide that combines tuition, living costs, and funding research for an Indian student planning to study in {city}, {destination_country} in {year}.

                TUITION RESEARCH:
                {tuition_result["data"]}

                COST OF LIVING RESEARCH:
                {living_result["data"]}

                FUNDING OPTIONS RESEARCH:
                {funding_result["data"]}

                ESTIMATED TOTAL ANNUAL COST: ${total_estimated_cost:,.2f}

                Create a comprehensive financial planning guide that combines all this information. Provide:

                1. **EXECUTIVE SUMMARY**:
                - Total estimated annual cost breakdown
                - Recommended funding strategy
                - Timeline for financial planning and applications
                - Key action items for the student

                2. **COMPLETE COST ANALYSIS**:
                - Academic costs (tuition, fees, books)
                - Living expenses (housing, food, transport, personal)
                - One-time costs (visa, deposits, setup, travel)
                - Annual total and 2-year program total

                3. **OPTIMAL FUNDING STRATEGY**:
                - Best 2-3 education loan recommendations
                - Loan amount vs self-funding ratio
                - EMI projections and repayment planning
                - Tax benefits and savings strategies
                - Scholarship opportunities to reduce loan burden

                4. **LOAN APPLICATION ROADMAP**:
                - Timeline: when to apply for loans
                - Documentation checklist
                - Multiple bank application strategy
                - Tips for loan approval
                - Backup funding options

                5. **F1 VISA FINANCIAL DOCUMENTATION**:
                - Exact I-20 amount requirements
                - Bank statement preparation
                - Loan sanction letter requirements
                - Sponsor documentation if needed
                - SEVIS fee and other visa costs

                6. **MONTHLY BUDGET & CASH FLOW**:
                - Pre-arrival costs breakdown
                - First semester detailed budget
                - Monthly living expenses tracking
                - Emergency fund recommendations
                - Currency exchange planning

                7. **RISK MITIGATION**:
                - What if loan is rejected?
                - Currency fluctuation protection
                - Emergency funding scenarios
                - Part-time work opportunities and limitations

                8. **GRADUATION & REPAYMENT PLANNING**:
                - Expected starting salary post-graduation
                - Loan repayment scenarios
                - OPT/H1B financial implications
                - Career ROI analysis

                Make this a complete, actionable financial blueprint that an Indian student can follow from decision to graduation.
                Include specific timelines, exact amounts, and step-by-step action items.
                """
                
                comprehensive_response = await self._run_agent(final_prompt)
                
                return {
                    "status": "success",
                    "comprehensive_plan": comprehensive_response,
                    "tuition_research": tuition_result,
                    "living_cost_research": living_result,
                    "funding_research": funding_result,
                    "estimated_total_cost": total_estimated_cost,
                    "city": city,
                    "year": year,
                    "university": university_name,
                    "destination_country": destination_country
                }
            else:
                # Return partial results if some research failed
                return {
                    "status": "partial_success",
                    "tuition_research": tuition_result,
                    "living_cost_research": living_result,
                    "funding_research": funding_result,
                    "estimated_total_cost": total_estimated_cost,
                    "city": city,
                    "year": year,
                    "university": university_name,
                    "destination_country": destination_country,
                    "message": "Some research components failed, but partial results available"
                }
                
        except Exception as e:
            logger.error(f"Error in comprehensive research: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "city": city,
                "year": year,
                "university": university_name,
                "destination_country": destination_country
            }
