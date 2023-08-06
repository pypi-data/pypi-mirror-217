from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
from typing import List
from zhixuewang.models import ExtendedList
from zhixuewang.teacher.models import Scores
from zhixuewang.teacher.tools import group_by, spread_array

def get_differ_property(data: List, f):
    a = []
    for i in data:
        temp = f(i)
        if temp not in a:
            a.append(temp)
    return a

def write_data(subject_names: List[str], scores: Scores, is_cross_exam: bool = False):
    wb = Workbook()
    sheet = wb.active
    colomn_names = ["姓名", "学校", "班级"]
    if len(subject_names) > 1:
        colomn_names.extend(["总分", "总分班级排名", "总分年级排名"])
        if is_cross_exam:
            colomn_names.append("总分联考排名")
    for subject_name in subject_names:
        colomn_names.extend(
            [subject_name, f"{subject_name}班级排名", f"{subject_name}年级排名"])
        if is_cross_exam:
            colomn_names.append(f"{subject_name}联考排名")
    sheet.append(colomn_names)
    personScoreMap = group_by(spread_array(scores), lambda t: t.person.id)
    for personScores in personScoreMap.values():
        personScores = ExtendedList(personScores)
        cur_person = personScores[0].person
        cur_colomn_data = [cur_person.name, cur_person.clazz.school.name, cur_person.clazz.name]
        if len(subject_names) > 1:
            total_score = personScores[-1]
            cur_colomn_data.extend(
                [total_score.score, total_score.class_rank, total_score.grade_rank])
            if is_cross_exam:
                cur_colomn_data.append(total_score.exam_rank)
        for subject_name in subject_names:
            cur_score = personScores.find(
                lambda t: t.subject.name == subject_name)
            if cur_score is None:
                cur_colomn_data.extend([0, 0, 0])
                if is_cross_exam:
                    cur_colomn_data.append(0)
            else:
                cur_colomn_data.extend(
                    [cur_score.score, cur_score.class_rank, cur_score.grade_rank])
                if is_cross_exam:
                    cur_colomn_data.append(cur_score.exam_rank)
        sheet.append(cur_colomn_data)
    subject_name = "-".join(subject_names)
    wb.save(f"{subject_name}.xlsx")
    