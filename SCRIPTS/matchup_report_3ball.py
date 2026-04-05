#!/usr/bin/env python3
"""
3-BALL MATCHUP REPORT GENERATOR

Reads 3-ball screener results and generates beautiful HTML report
showing component matchups + combined values + Kelly sizing
"""

import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'texas_childrens_round4_3ball_results_3ball.csv'

try:
    df = pd.read_csv(input_file)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3-Ball Matchup Analysis Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.95;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }

        .summary-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }

        .summary-card .label {
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        .summary-card .value {
            font-size: 1.8em;
            font-weight: 700;
            color: #667eea;
        }

        .matchups-container {
            padding: 40px;
        }

        .matchup-card {
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }

        .matchup-card:hover {
            border-color: #667eea;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        }

        .matchup-number {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .three-way-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .player-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .player-name {
            font-weight: 700;
            font-size: 1.05em;
            margin-bottom: 10px;
            color: #333;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            font-size: 0.9em;
            border-bottom: 1px solid #e9ecef;
        }

        .stat-row:last-child {
            border-bottom: none;
        }

        .stat-label {
            color: #6c757d;
            font-weight: 500;
        }

        .stat-value {
            font-weight: 700;
            color: #333;
        }

        .component-edges {
            background: #f0f7ff;
            padding: 15px;
            border-left: 4px solid #667eea;
            border-radius: 4px;
            margin-bottom: 20px;
        }

        .component-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 0.9em;
        }

        .component-label {
            color: #6c757d;
        }

        .component-edge {
            font-weight: 700;
            color: #667eea;
        }

        .combined-values {
            background: #fff8e1;
            padding: 20px;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
        }

        .combined-title {
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }

        .combined-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 0.95em;
        }

        .combined-player {
            font-weight: 600;
            color: #333;
        }

        .combined-value {
            font-weight: 700;
            font-size: 1.1em;
        }

        .best-pick {
            background: #e7f5ff;
            border: 2px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .best-pick-label {
            font-size: 0.85em;
            color: #667eea;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .best-pick-value {
            font-size: 1.3em;
            font-weight: 700;
            color: #667eea;
        }

        .footer {
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.95em;
            border-top: 1px solid #e9ecef;
        }

        @media (max-width: 768px) {
            .three-way-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>3-Ball Matchup Analysis</h1>
            <p>Component 2-Ball Edges + Combined Values + Kelly Sizing</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <div class="label">Total 3-Balls</div>
                <div class="value">""" + str(len(df)) + """</div>
            </div>
            <div class="summary-card">
                <div class="label">Kelly Picks</div>
                <div class="value">""" + str(len(df[df['action_type'] == 'KELLY'])) + """</div>
            </div>
            <div class="summary-card">
                <div class="label">Lean Picks</div>
                <div class="value">""" + str(len(df[df['action_type'] == 'LEAN'])) + """</div>
            </div>
            <div class="summary-card">
                <div class="label">Total 1/4 Kelly</div>
                <div class="value">""" + str(round(df[df['action_type'] == 'KELLY']['kelly_qtr'].sum(), 2)) + """%</div>
            </div>
        </div>

        <div class="matchups-container">
"""

    for idx, row in df.iterrows():
        action = row['action_type']
        quality = row['data_quality']

        best_pick_player = row['best_pick']
        best_edge = row['best_combined_edge']

        # Determine best pick color
        if best_pick_player == row['player_a']:
            best_name_a = f"<span style='color: #28a745; font-weight: 700;'>{row['player_a']}</span>"
            best_name_b = row['player_b']
            best_name_c = row['player_c']
        elif best_pick_player == row['player_b']:
            best_name_a = row['player_a']
            best_name_b = f"<span style='color: #28a745; font-weight: 700;'>{row['player_b']}</span>"
            best_name_c = row['player_c']
        else:
            best_name_a = row['player_a']
            best_name_b = row['player_b']
            best_name_c = f"<span style='color: #28a745; font-weight: 700;'>{row['player_c']}</span>"

        action_color = '#17a2b8' if action == 'KELLY' else '#ffc107'
        action_text = 'KELLY' if action == 'KELLY' else ('LEAN' if action == 'LEAN' else 'PASS')

        html += f"""
            <div class="matchup-card">
                <div class="matchup-number">#{int(row['matchup_num'])}</div>
                <div class="three-way-grid">
                    <div class="player-box">
                        <div class="player-name">{best_name_a}</div>
                        <div class="stat-row">
                            <span class="stat-label">Model:</span>
                            <span class="stat-value">{row['model_a']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Market:</span>
                            <span class="stat-value">{row['implied_a']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Samples:</span>
                            <span class="stat-value">N={int(row['n_a'])}</span>
                        </div>
                    </div>
                    <div class="player-box">
                        <div class="player-name">{best_name_b}</div>
                        <div class="stat-row">
                            <span class="stat-label">Model:</span>
                            <span class="stat-value">{row['model_b']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Market:</span>
                            <span class="stat-value">{row['implied_b']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Samples:</span>
                            <span class="stat-value">N={int(row['n_b'])}</span>
                        </div>
                    </div>
                    <div class="player-box">
                        <div class="player-name">{best_name_c}</div>
                        <div class="stat-row">
                            <span class="stat-label">Model:</span>
                            <span class="stat-value">{row['model_c']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Market:</span>
                            <span class="stat-value">{row['implied_c']:.1f}%</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Samples:</span>
                            <span class="stat-value">N={int(row['n_c'])}</span>
                        </div>
                    </div>
                </div>

                <div class="component-edges">
                    <div class="component-row">
                        <span class="component-label">{row['player_a']:.20} vs {row['player_b']:.20}</span>
                        <span class="component-edge">{row['edge_ab']:+.1f}pp</span>
                    </div>
                    <div class="component-row">
                        <span class="component-label">{row['player_a']:.20} vs {row['player_c']:.20}</span>
                        <span class="component-edge">{row['edge_ac']:+.1f}pp</span>
                    </div>
                    <div class="component-row">
                        <span class="component-label">{row['player_b']:.20} vs {row['player_c']:.20}</span>
                        <span class="component-edge">{row['edge_bc']:+.1f}pp</span>
                    </div>
                </div>

                <div class="combined-values">
                    <div class="combined-title">Combined 3-Ball Values</div>
                    <div class="combined-row">
                        <span class="combined-player">{row['player_a']}</span>
                        <span class="combined-value" style="color: {'#28a745' if row['best_pick'] == row['player_a'] else '#333'};">{row['combined_edge_a']:+.1f}pp</span>
                    </div>
                    <div class="combined-row">
                        <span class="combined-player">{row['player_b']}</span>
                        <span class="combined-value" style="color: {'#28a745' if row['best_pick'] == row['player_b'] else '#333'};">{row['combined_edge_b']:+.1f}pp</span>
                    </div>
                    <div class="combined-row">
                        <span class="combined-player">{row['player_c']}</span>
                        <span class="combined-value" style="color: {'#28a745' if row['best_pick'] == row['player_c'] else '#333'};">{row['combined_edge_c']:+.1f}pp</span>
                    </div>

                    <div class="best-pick">
                        <div class="best-pick-label">Best Pick</div>
                        <div class="best-pick-value">{row['best_pick']} ({row['best_combined_edge']:+.1f}pp)</div>
                        <div style="margin-top: 10px; font-size: 0.85em; color: #667eea;">
                            Data Quality: <strong>{row['data_quality']}</strong> |
                            Kelly: Full {row['kelly_full']:.2f}% -> 1/4 Kelly {row['kelly_qtr']:.2f}% |
                            Action: <strong style="color: {action_color};">{action_text}</strong>
                        </div>
                    </div>
                </div>
            </div>
"""

    html += """
        </div>

        <div style="padding: 40px; background: #f8f9fa; border-top: 1px solid #e9ecef;">
            <h2 style="color: #333; margin-bottom: 15px;">Analysis Summary</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: #667eea; font-size: 0.95em; margin-bottom: 10px; font-weight: 600;">Data Quality</h3>
                    <p style="font-size: 0.9em; margin-bottom: 6px;">Full: """ + str(len(df[df['data_quality'] == 'FULL'])) + """ (""" + str(round(len(df[df['data_quality'] == 'FULL'])/len(df)*100)) + """%)</p>
                    <p style="font-size: 0.9em; margin-bottom: 6px;">Limited: """ + str(len(df[df['data_quality'] == 'LIMITED'])) + """ (""" + str(round(len(df[df['data_quality'] == 'LIMITED'])/len(df)*100)) + """%)</p>
                    <p style="font-size: 0.9em;">Very Limited: """ + str(len(df[df['data_quality'] == 'VERY LIMITED'])) + """ (""" + str(round(len(df[df['data_quality'] == 'VERY LIMITED'])/len(df)*100)) + """%)</p>
                </div>
                <div>
                    <h3 style="color: #667eea; font-size: 0.95em; margin-bottom: 10px; font-weight: 600;">Actions</h3>
                    <p style="font-size: 0.9em; margin-bottom: 6px;">Kelly: """ + str(len(df[df['action_type'] == 'KELLY'])) + """ (""" + str(round(len(df[df['action_type'] == 'KELLY'])/len(df)*100)) + """%)</p>
                    <p style="font-size: 0.9em; margin-bottom: 6px;">Lean: """ + str(len(df[df['action_type'] == 'LEAN'])) + """ (""" + str(round(len(df[df['action_type'] == 'LEAN'])/len(df)*100)) + """%)</p>
                    <p style="font-size: 0.9em;">Pass: """ + str(len(df[df['action_type'] == 'PASS'])) + """ (""" + str(round(len(df[df['action_type'] == 'PASS'])/len(df)*100)) + """%)</p>
                </div>
            </div>
        </div>

        <div class="footer">
            <p><strong>3-Ball Matchup Analysis Report</strong></p>
            <p style="color: #999; font-size: 0.85em; margin-top: 10px;">Generated """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """ | Component 2-Ball Breakdown + Combined Values + Kelly Sizing</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = input_file.replace('_results_3ball.csv', '_report_3ball.html')
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"[OK] HTML report generated: {output_file}")
    print()

except FileNotFoundError:
    print(f"[!] File not found: {input_file}")
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
