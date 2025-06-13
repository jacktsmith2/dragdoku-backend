CRITERIA = [
{
    "label": "Season 1",
    "description": "Queen appeared in Season 1 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 1)"
},
{
    "label": "Season 2",
    "description": "Queen appeared in Season 2 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 2)"
},
{
    "label": "Season 3",
    "description": "Queen appeared in Season 3 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 3)"
},
{
    "label": "Season 4",
    "description": "Queen appeared in Season 4 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 4)"
},
{
    "label": "Season 5",
    "description": "Queen appeared in Season 5 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 5)"
},
{
    "label": "Season 6",
    "description": "Queen appeared in Season 6 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 6)"
},
{
    "label": "Season 7",
    "description": "Queen appeared in Season 7 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 7)"
},
{
    "label": "Season 8",
    "description": "Queen appeared in Season 8 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 8)"
},
{
    "label": "Season 9",
    "description": "Queen appeared in Season 9 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 9)"
},
{
    "label": "Season 10",
    "description": "Queen appeared in Season 10 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 10)"
},
{
    "label": "Season 11",
    "description": "Queen appeared in Season 11 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 11)"
},
{
    "label": "Season 12",
    "description": "Queen appeared in Season 12 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 12)"
},
{
    "label": "Season 13",
    "description": "Queen appeared in Season 13 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 13)"
},
{
    "label": "Season 14",
    "description": "Queen appeared in Season 14 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 14)"
},
{
    "label": "Season 15",
    "description": "Queen appeared in Season 15 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 15)"
},
{
    "label": "Season 16",
    "description": "Queen appeared in Season 16 (any franchise).",
    "sql": "queen_id IN (SELECT queen_id FROM queens WHERE season_no = 16)"
},
{
    "label": "Returning Queen",
    "description": "Queen returned to the competition during any season.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(is_returning) >= 1)"
},
{
    "label": "Multi-Season Queen",
    "description": "Queen appeared in more than one season.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING COUNT(DISTINCT season_no) > 1)"
},
{
    "label": "No Maxi Wins",
    "description": "Queen has zero maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) = 0)"
},
{
    "label": "1 Maxi Win",
    "description": "Queen has one maxi challenge win.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) = 1)"
},
{
    "label": "2 Maxi Wins",
    "description": "Queen has two maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) = 2)"
},
{
    "label": "3 Maxi Wins",
    "description": "Queen has three maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) = 3)"
},
{
    "label": "4 Maxi Wins",
    "description": "Queen has four maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) = 4)"
},
{
    "label": "1+ Maxi Win",
    "description": "Queen has at least one maxi challenge win.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) > 0)"
},
{
    "label": "2+ Maxi Wins",
    "description": "Queen has at least two maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) >= 2)"
},
{
    "label": "3+ Maxi Wins",
    "description": "Queen has at least three maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) >= 3)"
},
{
    "label": "4+ Maxi Wins",
    "description": "Queen has at least four maxi challenge wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(win) >= 4)"
},
{
    "label": "No Lip Sync Wins",
    "description": "Queen has zero lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) = 0)"
},
{
    "label": "1 Lip Sync Win",
    "description": "Queen has one lip sync win.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) = 1)"
},
{
    "label": "2 Lip Sync Wins",
    "description": "Queen has two lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) = 2)"
},
{
    "label": "3 Lip Sync Wins",
    "description": "Queen has three lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) = 3)"
},
{
    "label": "4 Lip Sync Wins",
    "description": "Queen has four lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) = 4)"
},
{
    "label": "1+ Lip Sync Win",
    "description": "Queen has at least one lip sync win.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) >= 1)"
},
{
    "label": "2+ Lip Sync Wins",
    "description": "Queen has at least two lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) >= 2)"
},
{
    "label": "3+ Lip Sync Wins",
    "description": "Queen has at least three lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) >= 3)"
},
{
    "label": "4+ Lip Sync Wins",
    "description": "Queen has at least four lip sync wins.",
    "sql": "queen_id IN (SELECT queen_id FROM queens GROUP BY queen_id HAVING SUM(lip_sync_wins) >= 4)"
}
]