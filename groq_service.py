import os
import json
import re
from groq import Groq
from config import Config

class GroqMarketingService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "") or Config.GROQ_API_KEY
        self.client = None
        if self.api_key and self.api_key != "gsk_your_groq_api_key_here":
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[GroqMarketingService] Warning initializing Groq client: {e}")
                self.client = None

    def refresh_client(self, new_api_key=None):
        if new_api_key:
            self.api_key = new_api_key
        else:
            self.api_key = os.getenv("GROQ_API_KEY", "")
        if self.api_key and self.api_key != "gsk_your_groq_api_key_here":
            try:
                self.client = Groq(api_key=self.api_key)
                return True
            except Exception:
                return False
        return False

    def is_configured(self):
        return bool(self.client and self.api_key and self.api_key != "gsk_your_groq_api_key_here")

    def _call_groq(self, system_prompt, user_prompt, temperature=0.7, json_mode=False):
        if not self.is_configured():
            return None
        try:
            kwargs = {
                "model": Config.GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 2048,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            
            chat_completion = self.client.chat.completions.create(**kwargs)
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"[Groq API Error]: {e}")
            return None

    # 1. AI Marketing Strategy Generator
    def generate_marketing_strategy(self, business_prompt, budget="₹50,000", industry="Retail"):
        system_prompt = """You are an elite CMO and AI Marketing Strategist. 
Analyze the user's business description and produce a structured marketing strategy in valid JSON.
Return JSON with the following keys:
{
  "target_audience": "detailed demographic, psychographic, and behavioral profile",
  "marketing_channels": ["Channel 1 (e.g. Instagram Reels)", "Channel 2 (e.g. Campus WhatsApp)", "Channel 3", "Channel 4"],
  "campaign_ideas": [
    {"name": "Campaign Title", "hook": "Hook description", "platform": "Platform", "expected_outcome": "Outcome"},
    {"name": "Campaign Title 2", "hook": "Hook description", "platform": "Platform", "expected_outcome": "Outcome"}
  ],
  "budget_distribution": [
    {"channel": "Channel Name", "percentage": 40, "amount": "₹20,000", "purpose": "Influencer seeding & UGC"},
    {"channel": "Channel Name", "percentage": 30, "amount": "₹15,000", "purpose": "Meta Ad targeting"}
  ],
  "marketing_goals": [
    "Primary Goal with specific metric (e.g. 5,000 college signups)",
    "Secondary Engagement Goal",
    "ROI Target"
  ],
  "summary": "Inspiring executive summary"
}
Output only valid JSON."""

        user_prompt = f"Business Details: {business_prompt}\nIndustry: {industry}\nTotal Budget: {budget}"
        response = self._call_groq(system_prompt, user_prompt, json_mode=True)
        
        if response:
            try:
                return json.loads(response)
            except Exception:
                pass

        # Fallback intelligent strategy
        return {
            "target_audience": "Students & Gen-Z young adults (aged 18–24), college campus influencers, trend-seekers who value self-expression, thrift aesthetics, and instant digital convenience.",
            "marketing_channels": [
                "Instagram Reels & Stories (UGC and styling hauls)",
                "Campus WhatsApp Communities & Student Council Partnerships",
                "YouTube Shorts (Behind-the-scenes & student transformation drops)",
                "Targeted Google Search (High-intent college festival queries)"
            ],
            "campaign_ideas": [
                {
                    "name": "College Fest Streetwear Drop",
                    "hook": "Ditch the boring formals—wear what speaks your campus vibe. Tag your college for 20% off!",
                    "platform": "Instagram & Campus Ambassador Network",
                    "expected_outcome": "15,000+ Reach and 600+ new first-order purchases"
                },
                {
                    "name": "Freshers Mystery Wardrobe Box",
                    "hook": "First week of college? Get 3 curated aesthetic fits for the price of 2 with student ID verification.",
                    "platform": "WhatsApp Groups & Micro-influencers",
                    "expected_outcome": "High viral shareability and 35% repeat purchase rate"
                },
                {
                    "name": "Style Challenge: Best Campus OOTD",
                    "hook": "Submit your 15-sec reel wearing our apparel to win ₹10,000 campus shopping spree.",
                    "platform": "Instagram Reels & TikTok",
                    "expected_outcome": "Over 200 user-generated video assets at zero ad production cost"
                }
            ],
            "budget_distribution": [
                {"channel": "Instagram Reels & Meta Ads", "percentage": 40, "amount": "₹20,000", "purpose": "Paid boost on top-performing organic reels and student lookbooks"},
                {"channel": "Campus Brand Ambassadors (Part-Time)", "percentage": 25, "amount": "₹12,500", "purpose": "Micro-stipends and commission rewards for college students"},
                {"channel": "Fest Sponsorship & Flash Giveaways", "percentage": 20, "amount": "₹10,000", "purpose": "Merchandise giveaways at college cultural and sports fests"},
                {"channel": "WhatsApp Marketing & SMS Automations", "percentage": 15, "amount": "₹7,500", "purpose": "Direct cart recovery and exclusive VIP drop alerts"}
            ],
            "marketing_goals": [
                "Generate 100,000+ targeted student impressions in 30 days",
                "Achieve 4.5x Return on Ad Spend (ROAS) across college festival season",
                "Onboard 15 active college student marketing affiliates across top 5 campuses"
            ],
            "summary": "This high-impact youth acquisition strategy leverages peer-to-peer campus marketing and viral short-form video hooks to maximize conversion while keeping customer acquisition cost (CAC) ultra-low."
        }

    # 2. AI Content Generator
    def generate_content(self, content_type, topic, tone="Energetic & Trendy", product_details=""):
        system_prompt = f"""You are a master creative copywriter.
Generate high-converting marketing content for the requested format: {content_type}.
Tone: {tone}
Return JSON with the following structure:
{{
  "content_type": "{content_type}",
  "primary_content": "The main copy ready to copy-paste",
  "variations": [
    "Alternative variation 1",
    "Alternative variation 2",
    "Alternative variation 3"
  ],
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "call_to_action": "Compelling CTA button text / ending prompt",
  "pro_tip": "Expert marketing tip for posting this content"
}}
Return only valid JSON."""

        user_prompt = f"Topic/Product: {topic}\nProduct Details: {product_details}\nTone: {tone}"
        response = self._call_groq(system_prompt, user_prompt, json_mode=True)
        if response:
            try:
                return json.loads(response)
            except Exception:
                pass

        # Robust Content Fallbacks
        content_map = {
            "Instagram Caption": {
                "primary_content": "Campus looks just got an upgrade 🔥 Say goodbye to wardrobe panic before 8 AM lectures. Our new oversized streetwear drop is officially live! Tap the link in bio to claim your exclusive student 20% discount with code: CAMPUSVIBE ⚡👇",
                "variations": [
                    "Not your ordinary college fit. Premium breathable cotton, statement graphics, and fits that turn heads in the canteen. Grab yours before the fest sellout! 🚀",
                    "Dressing well is a form of self-respect. Upgrade your daily rotation with pieces engineered for all-day comfort from classes to evening hangouts ✨",
                    "Warning: You will get asked 'Where did you get that?' at least 5 times today. Link in bio to cop the drop before stock vanishes 📦💨"
                ],
                "hashtags": ["#CampusStyle", "#CollegeOOTD", "#StreetwearVibes", "#StudentDiscount", "#CollegeLife", "#FestFashion", "#GenZStyle"],
                "call_to_action": "Tap link in bio to shop the drop with code CAMPUSVIBE ⚡",
                "pro_tip": "Post between 6:30 PM - 9:00 PM on weekdays when college students finish classes and scroll feeds."
            },
            "Ad Copy": {
                "primary_content": "Headline: Stop Overpaying For Trendy Fits 👕\nBody: High-quality, aesthetic streetwear designed for college budgets. Get 3 premium tees for just ₹999 + Free Delivery on campus orders! Over 10,000+ students already repping the brand.\nCTA: Shop Fest Sale Now",
                "variations": [
                    "Headline: Your Ultimate College Wardrobe Is Here 🎓\nBody: Turn everyday campus walks into your personal runway. Durable fabrics, bold prints, and unbeatable student pricing.\nCTA: Claim 20% Student Code",
                    "Headline: 8 AM Lecture Ready in 30 Seconds ⏰\nBody: Effortless comfort meets viral aesthetics. Discover our bestselling oversized collection today.\nCTA: Explore Best Sellers"
                ],
                "hashtags": ["#AdCopy", "#CollegeSale", "#StudentDeals", "#FashionDrop"],
                "call_to_action": "Click 'Shop Now' & Use Code 'COLLEGEFEST' for instant 20% off!",
                "pro_tip": "Use vertical 9:16 carousel video ads showing quick 3-second transitions for 3x higher click-through rates."
            },
            "Email Subject Lines": {
                "primary_content": "⚡ [URGENT] Exclusive 24-Hour Campus Flash Sale Starts NOW!",
                "variations": [
                    "Did someone say 20% off your entire college fest wardrobe? 👀",
                    "Your 8 AM lecture just got a massive style upgrade... 🚀",
                    "Psst... We left something in your bag (and added a surprise discount) 🎁",
                    "Final Call: Fest special mystery boxes are 90% claimed! ⏳"
                ],
                "hashtags": ["#EmailMarketing", "#OpenRateBooster"],
                "call_to_action": "Open to unlock your unique 1-time discount code",
                "pro_tip": "Keep subject lines under 45 characters and include an emoji in the first 3 characters for mobile inbox preview."
            },
            "Product Description": {
                "primary_content": "Crafted from 240 GSM 100% combed cotton, this Oversized Graphic Drop-Shoulder Tee blends timeless street culture with uncompromised daily comfort. Designed with reinforced ribbing at the neck and high-definition fade-proof screen prints, it stays pristine wash after wash. Pair with loose denims or cargo joggers for effortless campus cool.",
                "variations": [
                    "Minimalist, breathable, and designed for endless comfort. Featuring a relaxed drop-shoulder silhouette and premium French Terry fabric that moves with you through classes and late-night coding sessions.",
                    "The statement hoodie your feed has been waiting for. Double-stitched seams, roomy kangaroo pockets, and custom embroidered typography that stands out effortlessly."
                ],
                "hashtags": ["#ProductHighlight", "#StreetwearDaily", "#AestheticFits"],
                "call_to_action": "Add to Bag & Get Free Express Shipping across campuses!",
                "pro_tip": "Highlight fabric GSM, wash durability, and real sizing fit tips to slash return rates by up to 40%."
            },
            "Hashtags": {
                "primary_content": "#CampusFashion #CollegeOOTD #StreetwearIndia #StudentLife #FestVibes #AestheticOutfits #GraphicTees #GenZStyle",
                "variations": [
                    "#CollegeStyleGuide #DailyFits #BudgetFashion #CampusTrends #StudentDeals #UrbanWear #IndianStreetwear",
                    "#FashionOnABudget #CollegeFest #OOTDIndia #TrendingFits #CampusInfluencer #OutfitInspo"
                ],
                "hashtags": ["#ViralTags", "#ReachBooster"],
                "call_to_action": "Copy and paste into your first comment or reel caption!",
                "pro_tip": "Mix 3 high-volume tags (>1M posts), 5 niche community tags (10k-100k posts), and 2 brand-specific tags."
            },
            "Promotional Messages": {
                "primary_content": "Hey [Name]! 🎉 Got plans for the college fest? We've reserved an exclusive ₹300 voucher for you on orders above ₹1,000. Use code: VIPFEST at checkout today: marketmind.ai/shop. Offer expires at midnight! ⏳",
                "variations": [
                    "🔥 WhatsApp Flash Drop: Our limited edition oversized hoodies just restocked! Only 50 pieces available for campus delivery. Grab yours here: marketmind.ai/hoodies",
                    "Surprise! 🎁 Your loyalty points just unlocked a Free Graphic Canvas Tote with your next purchase. Claim before Sunday: marketmind.ai/rewards"
                ],
                "hashtags": ["#WhatsAppMarketing", "#SMSMarketing", "#FlashSale"],
                "call_to_action": "Reply 'YES' to receive your instant checkout link!",
                "pro_tip": "WhatsApp messages have a 98% open rate—keep the message concise with clear emojis and personal name token."
            }
        }
        return content_map.get(content_type, content_map["Instagram Caption"])

    # 3. AI Marketing Recommendation Engine (Innovative Part)
    def generate_recommendation_insights(self, performance_summary="Engagement dropped by 18% this month"):
        system_prompt = """You are an AI Growth Engine.
Given recent marketing performance metrics or issue alerts, generate precise, high-impact marketing recommendations.
Return JSON with the following schema:
{
  "alerts": [
    {
      "metric": "Engagement Rate",
      "issue": "Dropped by 18% over the last 30 days",
      "severity": "Warning",
      "recommendation": "Post short-form vertical reels 3–4 times per week targeting users aged 18–24 between 6 PM and 9 PM featuring behind-the-scenes student styling.",
      "estimated_impact": "+24% Engagement recovery in 14 days",
      "action_label": "Schedule Reel Campaign"
    },
    {
      "metric": "Instagram Ad Clicks",
      "issue": "Cost Per Click (CPC) rose by ₹4.20",
      "severity": "Alert",
      "recommendation": "Rotate ad creative: replace static product photos with real student customer video testimonials and unboxing hooks.",
      "estimated_impact": "-32% CPC reduction and higher click-through",
      "action_label": "Deploy UGC Testimonial Ads"
    },
    {
      "metric": "Cart Abandonment Rate",
      "issue": "64% of college visitors drop off at checkout",
      "severity": "Critical",
      "recommendation": "Trigger automated WhatsApp cart reminders 15 minutes after abandon offering 10% UPI instant cashback.",
      "estimated_impact": "+18% recovered cart revenue",
      "action_label": "Enable WhatsApp Automation"
    }
  ]
}
Output only valid JSON."""

        user_prompt = f"Performance Summary: {performance_summary}"
        response = self._call_groq(system_prompt, user_prompt, json_mode=True)
        if response:
            try:
                return json.loads(response)
            except Exception:
                pass

        return {
            "alerts": [
                {
                    "metric": "Engagement Rate",
                    "issue": "Dropped by 18% this month",
                    "severity": "Warning",
                    "recommendation": "Post short-form videos 3–4 times per week and target users aged 18–24 between 6 PM and 9 PM with trending audio hooks.",
                    "estimated_impact": "+25% engagement bounce back within 12 days",
                    "action_label": "Generate Video Campaign Hook"
                },
                {
                    "metric": "Conversion from Campus Traffic",
                    "issue": "High traffic from college Wi-Fi but low first-order completion",
                    "severity": "Alert",
                    "recommendation": "Introduce 1-click UPI checkout and offer an instant ₹150 student discount verified via college email/ID.",
                    "estimated_impact": "+3.4% conversion rate lift",
                    "action_label": "Activate Student Instant Promo"
                },
                {
                    "metric": "Affiliate Employee Output",
                    "issue": "Part-time student promoter sharing dropped by 12% during midterms",
                    "severity": "Info",
                    "recommendation": "Launch a 'Midterm De-stress Giveaway' where student promoters earn 2x commission per 10 orders referred.",
                    "estimated_impact": "Double campus affiliate outreach",
                    "action_label": "Boost Affiliate Incentives"
                }
            ]
        }

    # 4. Customer Segmentation Recommendations
    def get_segmentation_recommendations(self):
        return [
            {
                "segment": "New Customers",
                "characteristics": "First purchase within 30 days, high curiosity, exploring product range",
                "customer_count": 1240,
                "avg_spend": "₹850",
                "strategy": "Send a warm onboarding email & WhatsApp welcome message with an unboxing guide and a 15% discount on their second purchase valid for 14 days."
            },
            {
                "segment": "Loyal Customers",
                "characteristics": "5+ repeat purchases, frequent brand interactions, high NPS advocates",
                "customer_count": 480,
                "avg_spend": "₹4,200",
                "strategy": "Invite to an exclusive 'VIP Campus Club' with early 24-hour access to festival drops, free limited-edition merchandise, and a personalized referral code."
            },
            {
                "segment": "High Value Customers",
                "characteristics": "Top 10% spending tier (average basket > ₹3,500 per order)",
                "customer_count": 310,
                "avg_spend": "₹6,800",
                "strategy": "Provide premium concierge styling support, surprise gift additions in their packages, and invitations to co-design future streetwear capsule collections."
            },
            {
                "segment": "Inactive Customers",
                "characteristics": "No purchases or interactions for 90+ days",
                "customer_count": 890,
                "avg_spend": "₹620",
                "strategy": "Deploy a 'We Miss You' dynamic win-back campaign with a dramatic ₹250 instant credit and showcase your hottest new viral college arrivals."
            }
        ]

    # 5. Competitor Analysis & Differentiation
    def analyze_competitors(self, competitors_input):
        system_prompt = """You are a competitive intelligence marketing expert.
Analyze the competitors provided and output a structured JSON response:
{
  "competitor_insights": [
    {
      "name": "Competitor Name",
      "strength": "Their primary market strength",
      "weakness": "Their noticeable vulnerability",
      "your_edge": "How you can beat or out-maneuver them"
    }
  ],
  "differentiation_strategy": "A 3-step master strategy to uniquely position your business as the preferred choice"
}
Output only valid JSON."""

        user_prompt = f"Competitors to analyze: {competitors_input}"
        response = self._call_groq(system_prompt, user_prompt, json_mode=True)
        if response:
            try:
                return json.loads(response)
            except Exception:
                pass

        return {
            "competitor_insights": [
                {
                    "name": "UrbanCraze",
                    "strength": "Strong Instagram presence with 120k followers and high visual polish",
                    "weakness": "Slow customer service response and generic non-college focused themes",
                    "your_edge": "Hyper-local campus ambassadors who provide authentic peer-to-peer recommendations and same-day delivery to college hostels."
                },
                {
                    "name": "BudgetWear",
                    "strength": "Aggressive low pricing (₹399 graphic tees)",
                    "weakness": "Poor fabric durability, thin 160 GSM material, and high return rate",
                    "your_edge": "Position around 'Affordable Luxury'—heavyweight 240 GSM organic cotton that lasts 50+ washes for only a slight ₹100 price difference."
                },
                {
                    "name": "CampusChic",
                    "strength": "Strong customer reviews and alumni word-of-mouth",
                    "weakness": "Outdated marketing funnels with zero presence on short-form reels or WhatsApp",
                    "your_edge": "Modern Gen-Z video marketing, interactive TikTok/Reel challenges, and instant 1-click WhatsApp customer support."
                }
            ],
            "differentiation_strategy": "1. Community First: Build an active campus ambassador army where students wear and promote your drops. 2. Superior Quality Guarantee: Offer a '100-day print & fit guarantee' that outclasses low-budget rivals. 3. Hyper-Responsive Checkout: Implement instant WhatsApp & UPI checkout to capture high-intent impulsive mobile shoppers."
        }

    # 6. Part-Time Employee Task Matcher & Personalized Ad Suggestions
    def get_employee_matched_tasks(self, employee_interests="Instagram Reels, Meme Marketing"):
        interests_lower = employee_interests.lower()
        all_tasks = [
            {
                "id": 1,
                "title": "Create 3 Viral Instagram Reels for College Fest Drop",
                "channel": "Instagram",
                "tags": "Instagram Reels, Video Editing, Gen-Z",
                "reward_inr": 1500,
                "match_score": 98 if "reel" in interests_lower or "video" in interests_lower or "instagram" in interests_lower else 75,
                "description": "Shoot and edit 3 high-energy 15-second reels showcasing campus fits. Use trending college audio.",
                "ad_suggestion": "Hook: 'POV: You found the only streetwear brand that doesn't charge 3 months pocket money 😭🔥' -> Show quick fit switch in canteen."
            },
            {
                "id": 2,
                "title": "College WhatsApp Group & Status Broadcast Blast",
                "channel": "WhatsApp",
                "tags": "WhatsApp Groups, Campus Outreach, Student Clubs",
                "reward_inr": 800,
                "match_score": 95 if "whatsapp" in interests_lower or "outreach" in interests_lower else 70,
                "description": "Post custom curated promotional poster and affiliate link in 5 student/club WhatsApp groups.",
                "ad_suggestion": "Exclusive Campus Alert 📢: Hey guys! Grab ₹200 off your college fest outfit with student code [YOUR_NAME]20 at marketmind.ai/shop!"
            },
            {
                "id": 3,
                "title": "Design 2 College Relatable Meme Ads",
                "channel": "Instagram / Reddit",
                "tags": "Meme Marketing, Social Media, Design",
                "reward_inr": 1000,
                "match_score": 96 if "meme" in interests_lower or "social" in interests_lower else 65,
                "description": "Create humorous memes contrasting '8 AM Lecture Attendance' vs 'Fest Night Outfits' featuring our oversized tees.",
                "ad_suggestion": "Top Image: Attendance at 74.9%. Bottom Image: Me pulling up in this oversized graphic tee like I own the college."
            },
            {
                "id": 4,
                "title": "Campus Ambassador Flyer & QR Code Distribution",
                "channel": "Campus Outreach",
                "tags": "Campus Outreach, Event Sponsorships, College Fests",
                "reward_inr": 1200,
                "match_score": 92 if "outreach" in interests_lower or "event" in interests_lower else 60,
                "description": "Distribute 50 QR-coded discount postcards near college cafeteria and library notice boards.",
                "ad_suggestion": "Scan for Secret Student Wardrobe Drop & Free Sticker Pack!"
            }
        ]
        # Sort by match score descending
        all_tasks.sort(key=lambda x: x["match_score"], reverse=True)
        return all_tasks

    # 7. Pixie AI Chatbot Assistant
    def chat_with_pixie(self, user_message, chat_history=None, language="English"):
        system_prompt = f"""You are 'Pixie' ✨, the lovable, hyper-smart, and witty AI companion of MarketMind!
You look like a cute, animated girl mascot (inspired by adorable characters like Masha), full of positive energy, sparkling ideas, and playful wisdom.
Your mission:
1. Help users with marketing strategies, social media growth, campaign ideas, and copywriting.
2. Provide exceptional, accurate educational & college guidance (college fests, student clubs, study-work balance, internships, exam preparation, campus hacks).
3. Be enthusiastic, warm, supportive, and engaging. Sprinkle in delightful expressions and helpful structure!
4. Respond in the user's selected language: {language}.

IMPORTANT: You MUST format your response as valid JSON with this exact schema:
{{
  "reply": "Your helpful, enthusiastic response formatted in clean markdown with bullet points and emojis",
  "topic_category": "One of: campus | fashion | tech | creative | growth | coffee | celebration | general",
  "suggested_media": [
    {{"type": "image", "title": "Relevant Title", "keywords": "search term", "sample_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600&auto=format&fit=crop"}},
    {{"type": "video", "title": "Video Guide Title", "keywords": "video search term", "sample_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"}}
  ],
  "quick_followups": [
    "Follow-up question 1?",
    "Follow-up question 2?",
    "Follow-up question 3?"
  ]
}}
Return ONLY JSON."""

        history_context = ""
        if chat_history and isinstance(chat_history, list):
            for item in chat_history[-6:]:
                history_context += f"{item.get('sender', 'user')}: {item.get('message', '')}\n"

        prompt = f"Chat History:\n{history_context}\nCurrent User Message: {user_message}\nLanguage: {language}"
        response = self._call_groq(system_prompt, prompt, temperature=0.75, json_mode=True)
        
        if response:
            try:
                data = json.loads(response)
                return data
            except Exception:
                pass

        # Fallback Pixie Response Engine
        msg_lower = user_message.lower()
        topic = "general"
        media_img = "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600&auto=format&fit=crop&q=80"
        media_title = "Campus Community & Growth"
        
        if any(w in msg_lower for w in ["college", "study", "exam", "fest", "education", "student", "class", "university"]):
            topic = "campus"
            media_img = "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=600&auto=format&fit=crop&q=80"
            reply_text = f"✨ **Hey there, superstar! Pixie here!** 🎓\n\nCollege life is an incredible adventure where academics, creative passions, and future careers collide! Here is what you should keep in mind:\n\n1. 📚 **Mastering the Balance**: Treat your part-time marketing gigs like high-yield power sessions! 45 minutes of focused campus promotion + 90 minutes of lecture review = zero midterm stress!\n2. 🎪 **Campus Fest Magic**: College festivals are the #1 goldmine for student entrepreneurs. Set up live interactive booths, pass out sticker packs, and run instant QR-code giveaway contests.\n3. 🤝 **Network Exponentially**: The friends you collaborate with today in student clubs or marketing campaigns might be your future co-founders tomorrow!\n\nWhat college topic or campus marketing idea shall we brainstorm next?"
        elif any(w in msg_lower for w in ["fashion", "cloth", "store", "outfit", "wear", "dress", "style"]):
            topic = "fashion"
            media_img = "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=600&auto=format&fit=crop&q=80"
            reply_text = f"✨ **Ooh la la! Fashion is in the air!** 👗👟\n\nFor college streetwear and boutique fashion, here is Pixie's secret viral recipe:\n\n- 🔥 **Oversized & Heavyweight**: 240+ GSM graphic drops are reigning supreme in canteens and campus corridors.\n- 📸 **UGC Hauls Over Polished Studio Ads**: Students trust real peer lookbooks 10x more than sterile catalog shots! Have our student affiliates record 10-second 'How I style this tee for lectures' clips.\n- 🏷️ **Campus Ambassadors**: Give active college influencers their own personalized discount code (e.g. `PRIYA20`) and watch orders surge!\n\nWant me to write a viral reel script or design a promotional contest for this?"
        elif any(w in msg_lower for w in ["campaign", "ad", "instagram", "youtube", "whatsapp", "marketing", "strategy"]):
            topic = "growth"
            media_img = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&auto=format&fit=crop&q=80"
            reply_text = f"✨ **Growth mode activated!** 🚀📈\n\nLet's get those numbers climbing high! Here are Pixie's top 3 growth levers for you right now:\n\n1. 📲 **WhatsApp Broadcast Funnels**: Build a VIP student alert list with 98% open rates! Drop flash midnight offers.\n2. 🎬 **Vertical Video Blitz**: 3 short reels a week with trending audio beats any paid static banner by miles!\n3. 🎯 **Geo-Targeted Meta Ads**: Run radius ads within 5 km of local college campuses from 5 PM to 9 PM.\n\nReady to launch a new campaign? Just head over to our **Campaign Creator** or let me craft your ad copy!"
        else:
            topic = "creative"
            reply_text = f"✨ **Hello friend! I'm Pixie, your 24/7 AI Marketing & Campus Companion!** 💖\n\nI can help you build killer marketing strategies, craft viral captions, generate college campaign ideas, or even explain educational and academic concepts!\n\n**Quick things we can do together:**\n- 🎯 Generate a high-converting Instagram or WhatsApp campaign\n- 🎓 Brainstorm college fest marketing stunts\n- 📝 Write catchy ad copy, hashtags & product descriptions\n- 💡 Analyze your competitors and find your secret edge!\n\nWhat brilliant project are we working on right now?"

        return {
            "reply": reply_text,
            "topic_category": topic,
            "suggested_media": [
                {
                    "type": "image",
                    "title": media_title,
                    "keywords": topic,
                    "sample_url": media_img
                },
                {
                    "type": "video",
                    "title": "Interactive Campaign Preview",
                    "keywords": "marketing strategy video",
                    "sample_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
                }
            ],
            "quick_followups": [
                "How do I boost my Instagram engagement by 30%?",
                "Give me 5 viral campus marketing ideas for college fest",
                "What is the best way to earn part-time as a student promoter?"
            ]
        }

# Global singleton
groq_service = GroqMarketingService()
