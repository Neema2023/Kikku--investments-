FEATURED_VIP_PLANS = [
    {
        "name": "VIP 1",
        "amount": 5000,
        "daily_reward": 1000,
        "duration_days": 10,
        "style": "featured-yellow",
    },
    {
        "name": "VIP 2",
        "amount": 10000,
        "daily_reward": 2000,
        "duration_days": 10,
        "style": "featured-orange",
    },
    {
        "name": "VIP 3",
        "amount": 15000,
        "daily_reward": 3000,
        "duration_days": 10,
        "style": "featured-green",
    },
]

VIP_PLANS = [
    {
        "name": "VIP 4",
        "amount": 20000,
        "daily_reward": 4000,
        "duration_days": 10,
    },
    {
        "name": "VIP 5",
        "amount": 30000,
        "daily_reward": 6000,
        "duration_days": 10,
    },
    {
        "name": "VIP 6",
        "amount": 50000,
        "daily_reward": 9000,
        "duration_days": 15,
    },
    {
        "name": "VIP 7",
        "amount": 100000,
        "daily_reward": 12000,
        "duration_days": 15,
    },
    {
        "name": "VIP 8",
        "amount": 200000,
        "daily_reward": 23000,
        "duration_days": 15,
    },
    {
        "name": "VIP 9",
        "amount": 400000,
        "daily_reward": 35000,
        "duration_days": 15,
    },
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
        "description": "Send MTN MoMo to 0783108892 and upload your proof.",
    },
    {
        "step": 4,
        "title": "Verification",
        "description": "Admin verifies your payment screenshot.",
    },
    {
        "step": 5,
        "title": "Start Earning",
        "description": "VIP 1–5 earn daily for 10 days; VIP 6–9 for 15 days.",
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


def get_investment_duration(vip_name):
    plan = get_plan_by_name(vip_name)
    if plan:
        return plan.get("duration_days", 10)

    vip_number = get_vip_number(vip_name)
    if vip_number and vip_number <= 5:
        return 10
    return 15


def get_vip_number(vip_name):
    if not vip_name:
        return None
    parts = vip_name.strip().split()
    if len(parts) >= 2 and parts[-1].isdigit():
        return int(parts[-1])
    return None
