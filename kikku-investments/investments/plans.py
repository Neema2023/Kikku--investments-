FEATURED_VIP_PLANS = [
    {
        "name": "VIP 1",
        "amount": 5000,
        "daily_reward": 1000,
        "style": "featured-yellow",
    },
    {
        "name": "VIP 2",
        "amount": 10000,
        "daily_reward": 2000,
        "style": "featured-orange",
    },
    {
        "name": "VIP 3",
        "amount": 15000,
        "daily_reward": 3000,
        "style": "featured-green",
    },
]

VIP_PLANS = [
    {"name": "VIP 4", "amount": 20000, "daily_reward": 4000},
    {"name": "VIP 5", "amount": 30000, "daily_reward": 6000},
    {"name": "VIP 6", "amount": 50000, "daily_reward": 9000},
    {"name": "VIP 7", "amount": 100000, "daily_reward": 12000},
    {"name": "VIP 8", "amount": 200000, "daily_reward": 23000},
    {"name": "VIP 9", "amount": 400000, "daily_reward": 32000},
]

HOW_IT_WORKS = [
    {
        "step": 1,
        "title": "Register",
        "description": "Create your account using your phone number.",
    },
    {
        "step": 2,
        "title": "Choose VIP",
        "description": "Select an investment package that fits your budget.",
    },
    {
        "step": 3,
        "title": "Send Payment",
        "description": "Deposit using MTN MoMo and upload proof.",
    },
    {
        "step": 4,
        "title": "Verification",
        "description": "Admin verifies payment manually.",
    },
    {
        "step": 5,
        "title": "Start Earning",
        "description": "Receive daily rewards according to your VIP plan.",
    },
]


def get_all_vip_plans():
    plans = []
    for plan in FEATURED_VIP_PLANS:
        plans.append(dict(plan))
    for plan in VIP_PLANS:
        plans.append(dict(plan))
    return plans


def get_plan_by_name(name):
    for plan in get_all_vip_plans():
        if plan["name"] == name:
            return plan
    return None


def get_vip_plan_choices():
    return [(p["name"], p["name"]) for p in get_all_vip_plans()]
