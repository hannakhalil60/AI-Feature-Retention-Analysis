**AI Feature Retention Analysis
**
Individual project for an MBA course in programming and data analytics (ASU W. P. Carey, 2026), using a course-provided case dataset for a fictional software company, Synapse Workspace.

**The question
**
Active users grew 11–35% for all five of the company's AI features over twelve months. That looks like success. I wanted to know whether people were actually coming back, or whether growth was hiding a retention problem.

Is the share of users who return to each AI feature rising or falling, and which features retain users best?
Is the pattern specific to certain features, or does it hold across the platform?
**Data**

Three course-provided files covering five AI features over twelve months: monthly usage (active, new, and returning users), customer feedback and ratings, and a feature catalog.

Before analyzing, I checked for duplicates and missing values (none) and confirmed that new plus returning users equals active users in every row. That check showed returning share and new-user share are mirror images, so I kept only one. I also found that the catalog's launch dates contradicted the usage data, so I left launch timing out instead of guessing which source was right.

**Findings
**

Returning share fell for every feature, by 7.7 to 9.1 points between the first and last six months. A paired t-test confirmed the drop wasn't chance (t = 33.20, p < 0.001).
The decline was platform-wide. All five features fell by nearly the same amount, and feature complexity explained none of the difference (82.6% vs. 82.2%).
Ratings would have missed it. Average ratings held at about 3.9–4.0 and drifted slightly up while returning share fell. The two were uncorrelated (r = −0.092, p = 0.485).
The decline wasn't users leaving. Returning users actually grew from 235 to 252. New users grew from 30 to 81, so the share fell because its denominator grew faster. Usage per active user also rose, from 1.45 to 2.38.
What I got wrong, and how I caught it

My first interpretation was that growth came from first-time users while fewer people came back. To check myself, I gave ChatGPT the same data and questions but none of my findings, and asked for an independent analysis. It split the ratio into its parts and showed that returning users had grown. I had read a change in user mix as a loss of users. I revised my conclusion and my recommendations.

**What I learned about using AI for analysis
**

Order matters. I'd used Claude to review my analysis plan, but it had already run the analysis, so it suggested tests it knew would come out significant. Its advice was useful, but it wasn't neutral. It also led me to reframe my second question in a way that ruled out a possible null result. Next time, I'll share my plan before sharing the data.
The most useful AI suggestions were about what not to do: dropping a redundant metric, skipping text analysis on five repeated sentences, and leaving out the contradictory launch dates.
I rejected one suggestion. A correlation between returning share and usage (r = −0.52) looked meaningful, but both variables trend with time, so month likely drives both.
AI was good at checking whether an analysis was sound. Deciding which result mattered to a product manager was still my job.

**Recommendations
**

Report new, returning, and active users as separate numbers, not one ratio.
Focus on turning new users into repeat users, rather than fixing individual features.
Don't use satisfaction ratings as an early warning for retention. They missed this pattern entirely.
Move to cohort tracking with individual user histories.
**Limitations
**

The data is monthly totals, not individual user histories, so returning share isn't true retention. It can't show whether the same people came back.
Five features over twelve months supports direction, not modeling.
All findings are correlational.
Ratings come only from users engaged enough to respond, so users who stopped returning are underrepresented.
**Files
**

Assignment_2_HannaKhalil.ipynb: data preparation and analysis
Assignment_3_HK.ipynb: visualizations and the independent AI comparison
