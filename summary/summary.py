import requests
import json
import webbrowser
import tempfile
import os, sys
from auth import auth
from dataclasses import dataclass
from datetime import datetime, time, date, timedelta
from zoneinfo import ZoneInfo
from jinja2 import Template

endpoint = "https://sicp.pascal-lab.net/api"
auth = auth()
token = auth["token"]
userId = auth["userId"]
fullName = auth["fullName"]

if len(sys.argv) == 2:
    userId = sys.argv[1]

session = requests.session()
session.headers.update(
    {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">

<head>
    <link rel="icon" href="https://sicp.pascal-lab.net/2025/favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SICP 年终总结 2025</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', 'Arial', sans-serif;
            background: linear-gradient(135deg, #7b2683 0%, #a84da8 50%, #7b2683 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #fff;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            color: #333;
        }

        .header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 3px solid #7b2683;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 3em;
            color: #7b2683;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(123, 38, 131, 0.1);
        }

        .header .subtitle {
            font-size: 1.3em;
            color: #a84da8;
            font-weight: 300;
        }

        .section {
            margin: 35px 0;
            padding: 25px;
            background: linear-gradient(to right, rgba(123, 38, 131, 0.05), rgba(168, 77, 168, 0.05));
            border-left: 4px solid #7b2683;
            border-radius: 8px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .section:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(123, 38, 131, 0.2);
        }

        .section p {
            font-size: 1.3em;
            line-height: 1.8;
            color: #444;
            margin: 8px 0;
        }

        .highlight {
            color: #7b2683;
            font-weight: bold;
            font-size: 1.15em;
            text-shadow: 1px 1px 2px rgba(123, 38, 131, 0.1);
        }

        .emoji {
            font-size: 1.5em;
            display: inline-block;
            margin: 0 5px;
        }

        .special-moment {
            background: linear-gradient(135deg, #7b2683, #a84da8);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 40px 0;
            box-shadow: 0 10px 30px rgba(123, 38, 131, 0.4);
        }

        .special-moment p {
            color: white;
            font-size: 1.4em;
            margin: 10px 0;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(123, 38, 131, 0.15);
            border-top: 4px solid #7b2683;
            text-align: center;
        }

        .stat-card .number {
            font-size: 2.5em;
            color: #7b2683;
            font-weight: bold;
            margin: 10px 0;
        }

        .stat-card .label {
            font-size: 1.1em;
            color: #666;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }

        .footer p {
            font-size: 1.3em;
            color: #7b2683;
            margin: 15px 0;
            font-weight: 500;
        }

        .footer .signature {
            font-size: 1.5em;
            margin-top: 20px;
            color: #a84da8;
        }

        @media (max-width: 768px) {
            .container {
                padding: 30px 20px;
            }

            .header h1 {
                font-size: 2em;
            }

            .section p {
                font-size: 1.1em;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <h1>🎓 {{full_name}} 的 SICP 年终总结</h1>
            <div class="subtitle">2025 · 与代码共舞的日子</div>
        </div>

        <div class="section">
            <p>今年你一共做过 <span class="highlight">{{ total_problems }}</span> 道题</p>
            <p>共计 <span class="highlight">{{ total_hours }}小时{{ total_minutes }}分钟</span></p>
            <p style="margin-top: 15px; color: #666; font-style: italic;">每个重要时刻，SICP都在场 <span class="emoji">📚</span>
            </p>
        </div>

        <div class="section">
            <p style="text-align: center; font-size: 1.4em; color: #7b2683;">
                <span class="emoji">🗺️</span> 在编程的旷野里你发现了新大陆 <span class="emoji">✨</span>
            </p>
        </div>

        <div class="section">
            <p>今年你一共提交了 <span class="highlight">{{ total_assignments }}</span> 次作业</p>
            <p>其中 <span class="highlight">{{ favorite_assignment }}</span> 是你的最爱，共提交了 <span class="highlight">{{
                    favorite_submissions }}</span> 次</p>
            <p style="margin-top: 15px; color: #666; font-style: italic;">简直挖到宝啦！<span class="emoji">💎</span></p>
        </div>

        <div class="special-moment">
            <p><span class="emoji">🌙</span>
                {{ late_night_month }}月{{ late_night_day }}日{{ late_night_hour }}点，你还在奋战</p>
            <p>梦境飘出了窗外</p>
            <p>那一夜的 {{ late_night_problem }} 一定很难忘 <span class="emoji">💪</span></p>
        </div>

        <div class="section">
            <p>{{ retry_month }}月{{ retry_day }}日，你提交了 <span class="highlight">{{ retry_times }}</span> 次作业，那是 <span class="highlight">{{ retry_problem }}</span> </p>
            <p style="margin-top: 15px; color: #7b2683; font-weight: bold;">再试一次！下一次一定成功！<span class="emoji">🚀</span>
            </p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{{ favorite_part_of_day }}</div>
                <div class="label">你最爱提交 OJ 的时间</div>
            </div>
            <div class="stat-card">
                <div class="number">{{ active_start }}:00-{{ active_end }}:00</div>
                <div class="label">本学期最活跃时间段</div>
            </div>
        </div>

        <div class="section">
            <p>5位助教中，<span class="highlight">{{ favorite_ta }}</span> 的题目对你而言最 Evil 😈</p>
            <p>你一共向 ta 的题目提交了 <span class="highlight">{{ ta_submissions }}</span> 次</p>
            <p style="margin-top: 15px; color: #666; font-style: italic;">真不容易！感谢你的坚持！<span class="emoji">🙏</span></p>
        </div>

        <div class="footer">
            <p><span class="emoji">🎉</span> 在你的参与下，你和 SICP 的故事才完整 <span class="emoji">💜</span></p>
            <p class="signature">—— 愿你在编程的道路上越走越远 ——</p>
        </div>
    </div>
</body>

</html>
"""


@dataclass
class Submission:
    slug: str
    time: datetime
    score: int
    passed: bool


def retrieve_submissions(slug: str):
    print(f"Retrieving {slug}")
    response = session.get(
        f"{endpoint}/submissions",
        params={
            "page": "0",
            "size": "1",
            "assignmentId": slug,
            "userId": userId,
        },
    )
    assert response.ok, "Request failed!"
    submissions = json.loads(response.text)
    response = session.get(
        f"{endpoint}/submissions",
        params={
            "page": "0",
            "size": str(max(1, submissions["totalElements"])),
            "assignmentId": slug,
            "userId": userId,
        },
    )
    assert response.ok, "Request failed!"
    submissions = json.loads(response.text)

    for submission in submissions["content"]:
        score = submission["result"]["score"]
        utc_time = datetime.fromisoformat(
            submission["createdAt"].replace("Z", "+00:00")
        )
        china_time = utc_time.astimezone(ZoneInfo("Asia/Shanghai"))
        yield Submission(
            slug=slug,
            time=china_time,
            score=score,
            passed=True,
        )


problems = [
    "lab00",
    "lab01",
    "lab02",
    "lab03",
    "lab04",
    "lab05",
    "lab06",
    "lab07",
    "lab08",
    "lab09",
    "lab10",
    "hw01",
    "hw02",
    "hw03",
    "hw04",
    "hw05",
    "hw06",
    "hw07",
    "hw08",
    "hw09",
    "hw10",
    "proj01",
    "proj02",
    "proj03",
    "proj04",
]

slug_to_authors = {
    "lab00": "Jacy",
    "lab01": "jjppp",
    "lab02": "naiiren",
    "lab03": "yinfeng",
    "lab04": "yinfeng",
    "lab05": "Jacy",
    "lab06": "jjppp",
    "lab07": "naiiren",
    "lab08": "isla",
    "lab09": "isla",
    "lab10": "yinfeng",
    "hw01": "yinfeng",
    "hw02": "Jacy",
    "hw03": "jjppp",
    "hw04": "naiiren",
    "hw05": "isla",
    "hw06": "naiiren",
    "hw07": "isla",
    "hw08": "yinfeng",
    "hw09": "jjppp",
    "hw10": "Jacy",
    "proj01": "Jacy",
    "proj02": "yinfeng",
    "proj03": "naiiren",
    "proj04": "jjppp",
}


def my_main():
    all_submissions: list[Submission] = list(
        submission
        for per_problem in map(retrieve_submissions, problems)
        for submission in per_problem
    )

    slug_to_submissions: dict[str, list[Submission]] = {}
    for submission in all_submissions:
        if submission.slug not in slug_to_submissions:
            slug_to_submissions[submission.slug] = []
        slug_to_submissions[submission.slug].append(submission)

    total_problems = len(slug_to_submissions.keys())
    total_time: timedelta = sum(
        (
            max(
                timedelta(minutes=30),
                max(submissions, key=lambda x: x.time).time
                - min(submissions, key=lambda x: x.time).time,
            )
            for submissions in slug_to_submissions.values()
        ),
        timedelta(),
    )
    total_hours = total_time.days * 24 + total_time.seconds // 3600
    total_minutes = total_time.seconds % 3600 // 60
    total_submissions = len(all_submissions)

    late_submissions = list(
        filter(
            lambda s: time(18, 0, 0) <= s.time.time() or s.time.time() <= time(4, 0, 0),
            all_submissions,
        )
    )
    latest_submission: Submission = late_submissions[0]
    for submission in late_submissions:
        if time(21, 0, 0) <= latest_submission.time.time() <= submission.time.time():
            latest_submission = submission
        elif latest_submission.time.time() <= submission.time.time() <= time(4, 0, 0):
            latest_submission = submission

    favorite: str = all_submissions[0].slug
    for slug, submissions in slug_to_submissions.items():
        if len(submissions) > len(slug_to_submissions[favorite]):
            favorite = slug

    date_to_submissions: dict[date, list[Submission]] = {}
    for submission in all_submissions:
        if submission.time.date() not in date_to_submissions:
            date_to_submissions[submission.time.date()] = []
        date_to_submissions[submission.time.date()].append(submission)
    max_retry = list(date_to_submissions.keys())[0]
    for d, submissions in date_to_submissions.items():
        if len(submissions) > len(date_to_submissions[max_retry]):
            max_retry = d

    record = 0
    favorite_start = 0
    favorite_end = 2
    for start in range(22):
        end = start + 2
        if end > 24:
            end -= 24

        count = len(list(filter(lambda x: start <= x.time.hour < end, all_submissions)))
        if count > record:
            record = count
            favorite_start = start
            favorite_end = end

    count = len(
        list(filter(lambda x: 23 <= x.time.hour or x.time.hour < 1, all_submissions))
    )
    if count > record:
        record = count
        favorite_start = start
        favorite_end = end

    def get_part_of_day(hour):
        if 5 <= hour < 12:
            return "早晨"
        elif 12 <= hour < 17:
            return "下午"
        elif 17 <= hour < 21:
            return "晚上"
        else:
            return "深夜"

    favorite_part_of_day = get_part_of_day(favorite_start)

    author_to_submissions: dict[str, list[Submission]] = {}

    for submission in all_submissions:
        author_name = slug_to_authors[submission.slug]
        if author_name not in author_to_submissions:
            author_to_submissions[author_name] = []
        author_to_submissions[author_name].append(submission)

    favorite_author = list(author_to_submissions.keys())[0]
    for author, submissions in author_to_submissions.items():
        if len(submissions) > len(author_to_submissions[favorite_author]):
            favorite_author = author

    data = {
        "full_name": fullName,
        # 基础统计
        "total_problems": total_problems,  # 今年做过的题目总数
        "total_hours": total_hours,  # 总小时数
        "total_minutes": total_minutes,  # 总分钟数
        # 作业相关
        "total_assignments": total_submissions,  # 完成的作业次数
        "favorite_assignment": favorite,  # 最喜欢的作业
        "favorite_submissions": len(
            slug_to_submissions[favorite]
        ),  # 最喜欢作业的提交次数
        # 知识点
        "top_knowledge": "递归与高阶函数",  # 年度TOP知识点 TODO
        "code_soul": "函数式编程",  # "码魂"类型 TODO
        # 深夜奋战记录
        "late_night_month": latest_submission.time.month,  # 深夜奋战的月份
        "late_night_day": latest_submission.time.day,  # 深夜奋战的日期
        "late_night_hour": latest_submission.time.hour,  # 深夜奋战的小时
        "late_night_problem": latest_submission.slug,  # 那晚做的题目
        # 重试记录
        "retry_month": max_retry.month,  # 多次提交的月份
        "retry_day": max_retry.day,  # 多次提交的日期
        "retry_problem": ", ".join(
            set(map(lambda s: s.slug, date_to_submissions[max_retry]))
        ),  # 提交的题目名称 TODO
        "retry_times": len(date_to_submissions[max_retry]),  # 提交次数
        # 时间偏好
        "favorite_part_of_day": favorite_part_of_day,  # 最活跃的时间段
        "active_start": favorite_start,  # 最活跃时间段开始
        "active_end": favorite_end,  # 最活跃时间段结束
        # 助教相关
        "favorite_ta": favorite_author,  # 最喜欢的助教
        "ta_submissions": len(
            author_to_submissions[favorite_author]
        ),  # 向该助教题目提交的次数
    }
    output_file = "summary.html"

    # 创建Jinja2模板对象
    template = Template(HTML_TEMPLATE)

    # 渲染模板
    html_content = template.render(**data)

    # 保存生成的HTML文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 年终总结HTML已生成: {output_file}")
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        f.write(html_content)
        file_url = "file://" + os.path.abspath(f.name)
        webbrowser.open_new(file_url)
    return all_submissions


if __name__ == "__main__":
    submissions = my_main()
