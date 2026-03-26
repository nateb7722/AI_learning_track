This file contains a description of my nfl project, including the goals of the project, the data I am using, and the current state of the project. This can help you understand how to apply new concepts to this project, and also give you an understanding of the types of data I am working with. All data for this project is stored in s3

The project I have been working on has two primary end goals:

Analytics for Consumers - Provide analytics for all levels of sports betters that will give them a unique view of team and player performance. This will include relevant stats and trends for different bets as well.

Betting support & recommendations - Provide probability distributions for different outcomes (spread, total score, receiving yards, etc.) with insight into what factors are important for a given bet and adjustable priors. This will also include bet tracking, analysis of past bets, and sharing of bets.


The Analytics:

The core of my analytics approach is around discovering a team’s “true performance”. Every game has several factors, from weather to injuries to unlikely plays that force a team to change their strategy. This can turn a team's recorded performance into a situational performance. When situations change, a team's performance can vary greatly. When we can better estimate what the true performance would be, we can then model the possibilities for different situational performances. 
Instead of using yards or points to measure team performance, most of the charting will be based off of EPA (expected points added).

These analytics come from using:
play by play data
Roster data
Depth chart data
player activity data - snap counts, blitz, man vs zone coverage
player grades from PFF
Team and coaching level information 

This combines and aggregates into:
Player level data
Team & week level data
Team & season level data
Team & in-game level data (quarter, drive, half, etc.)
Game data
Coaching data

Aside from coaching data, all of this is accessible. I can download the data if it is needed for an example.

This turns into strength-of-schedule modeling, true injury impact modeling, and a better assessment of “true performance”. In addition to the analytics on performance, I will use ML / AI to discover what trends are actually important for a game, and display those for users. This part of the project will result in charts, stats, and important trends displayed on a website.


Betting Support & Recommendations:
I will build  Bayesian Hierarchical Models, built upon causal analysis of the relationships between variables, to provide probability distributions for different bets. This should include conditional modeling that would allow me to model the posterior probabilities for end-game state bets like spread or total points, given a certain early game data . For example, I should be able to answer questions like “what if team X has success running the ball early?”, or “what if team Y scores first?”, “what if team X is winning by 7 points at the end of the first quarter?”.