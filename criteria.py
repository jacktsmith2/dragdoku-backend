    CRITERIA = [
{
    "label": "Season 1",
    "description": "Queen appeared in Season 1 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 1)",
    "category": "season"
},
{
    "label": "Season 2",
    "description": "Queen appeared in Season 2 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 2)",
    "category": "season"
},
{
    "label": "Season 3",
    "description": "Queen appeared in Season 3 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 3)",
    "category": "season"
},
{
    "label": "Season 4",
    "description": "Queen appeared in Season 4 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 4)",
    "category": "season"
},
{
    "label": "Season 5",
    "description": "Queen appeared in Season 5 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 5)",
    "category": "season"
},
{
    "label": "Season 6",
    "description": "Queen appeared in Season 6 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 6)",
    "category": "season"
},
{
    "label": "Season 7",
    "description": "Queen appeared in Season 7 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 7)",
    "category": "season"
},
{
    "label": "Season 8",
    "description": "Queen appeared in Season 8 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 8)",
    "category": "season"
},
{
    "label": "Season 9",
    "description": "Queen appeared in Season 9 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 9)",
    "category": "season"
},
{
    "label": "Season 10",
    "description": "Queen appeared in Season 10 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 10)",
    "category": "season"
},
{
    "label": "Season 11",
    "description": "Queen appeared in Season 11 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 11)",
    "category": "season"
},
{
    "label": "Season 12",
    "description": "Queen appeared in Season 12 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 12)",
    "category": "season"
},
{
    "label": "Season 13",
    "description": "Queen appeared in Season 13 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 13)",
    "category": "season"
},
{
    "label": "Season 14",
    "description": "Queen appeared in Season 14 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 14)",
    "category": "season"
},
{
    "label": "Season 15",
    "description": "Queen appeared in Season 15 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 15)",
    "category": "season"
},
{
    "label": "Season 16",
    "description": "Queen appeared in Season 16 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 16)",
    "category": "season"
},
{
    "label": "Season 17",
    "description": "Queen appeared in Season 17 (any franchise).",
    "sql": "id IN (SELECT id FROM queens WHERE season_no = 17)",
    "category": "season"
},
{
    "label": "Returning Queen",
    "description": "Queen returned to the competition during any season.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(is_returning) >= 1)",
    "category" : "appearances"
},
{
    "label": "Multi-Season Queen",
    "description": "Queen appeared in more than one season.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING COUNT(DISTINCT season_no) > 1)",
    "category" : "appearances"
},
{
    "label": "No Mini Wins",
    "description": "Queen has zero mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) = 0)",
    "category" : "mini_wins",
    "min" : 0,
    "max" : 0
},
{
    "label": "1 Mini Win",
    "description": "Queen has one mini challenge win.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) = 1)",
    "category" : "mini_wins",
    "min" : 1,
    "max" : 1
},
{
    "label": "2 Mini Wins",
    "description": "Queen has two mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) = 2)",
    "category" : "mini_wins",
    "min" : 2,
    "max" : 2
},
{
    "label": "3 Mini Wins",
    "description": "Queen has three mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) = 3)",
    "category" : "mini_wins",
    "min" : 3,
    "max" : 3
},
{
    "label": "4 Mini Wins",
    "description": "Queen has four mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) = 4)",
    "category" : "mini_wins",
    "min" : 4,
    "max" : 4
},
{
    "label": "1+ Mini Win",
    "description": "Queen has at least one mini challenge win.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) > 0)",
    "category" : "mini_wins",
    "min" : 1,
    "max" : 999
},
{
    "label": "2+ Mini Wins",
    "description": "Queen has at least two mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) >= 2)",
    "category" : "mini_wins",
    "min" : 2,
    "max" : 999
},
{
    "label": "3+ Mini Wins",
    "description": "Queen has at least three mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) >= 3)",
    "category" : "mini_wins",
    "min" : 3,
    "max" : 999
},
{
    "label": "4+ Mini Wins",
    "description": "Queen has at least four mini challenge wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(win) >= 4)",
    "category" : "mini_wins",
    "min" : 4,
    "max" : 999
},
{
    "label": "No Lip Sync Wins",
    "description": "Queen has zero lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) = 0)",
    "category" : "lipsync_wins",
    "min" : 0,
    "max" : 0
},
{
    "label": "1 Lip Sync Win",
    "description": "Queen has one lip sync win.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) = 1)",
    "category" : "lipsync_wins",
    "min" : 1,
    "max" : 1
},
{
    "label": "2 Lip Sync Wins",
    "description": "Queen has two lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) = 2)",
    "category" : "lipsync_wins",
    "min" : 2,
    "max" : 2
},
{
    "label": "3 Lip Sync Wins",
    "description": "Queen has three lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) = 3)",
    "category" : "lipsync_wins",
    "min" : 3,
    "max" : 3
},
{
    "label": "4 Lip Sync Wins",
    "description": "Queen has four lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) = 4)",
    "category" : "lipsync_wins",
    "min" : 4,
    "max" : 4
},
{
    "label": "1+ Lip Sync Win",
    "description": "Queen has at least one lip sync win.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) >= 1)",
    "category" : "lipsync_wins",
    "min" : 1,
    "max" : 999
},
{
    "label": "2+ Lip Sync Wins",
    "description": "Queen has at least two lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) >= 2)",
    "category" : "lipsync_wins",
    "min" : 2,
    "max" : 999
},
{
    "label": "3+ Lip Sync Wins",
    "description": "Queen has at least three lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) >= 3)",
    "category" : "lipsync_wins",
    "min" : 3,
    "max" : 999
},
{
    "label": "4+ Lip Sync Wins",
    "description": "Queen has at least four lip sync wins.",
    "sql": "id IN (SELECT id FROM queens GROUP BY id HAVING SUM(lip_sync_wins) >= 4)",
    "category" : "lipsync_wins",
    "min" : 4,
    "max" : 999
}
]
