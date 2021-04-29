from django.core.serializers.json import DjangoJSONEncoder

from core.aux import generate_slug
from core.models import Skill, SkillCategory, Interest, InterestCategory
from members.models import Member, MemberSkill, MemberSkillCategory, MemberInterest, MemberInterestCategory


def add_skill_generic(tag, user):
    skill = Skill.objects.get(slug=tag)
    slug = generate_slug(MemberSkill)
    member = Member.objects.get(user=user)
    is_already = MemberSkill.objects.filter(member=member).filter(skill=skill)
    category_slug = SkillCategory.objects.filter(skill=skill)[0].slug
    current_category = SkillCategory.objects.get(slug=category_slug)
    if is_already.count() == 0:
        skill_slug = tag
        new_skill = MemberSkill(slug=slug, skill=skill, member=member,
                                category_slug=category_slug, skill_slug=skill_slug)
        new_skill.save()
        is_already = MemberSkillCategory.objects.filter(category=current_category).filter(member=member)
        # messages.success("Se añadió un skill al usuario.")
        if is_already.count() == 0:
            new_slug = generate_slug(MemberSkillCategory)
            new_category = MemberSkillCategory(slug=new_slug, category=current_category, member=member)
            new_category.save()
    return 1


def add_interest_generic(tag, user):
    interest = Interest.objects.get(slug=tag)
    slug = generate_slug(MemberInterest)
    member = Member.objects.get(user=user)
    is_already = MemberInterest.objects.filter(member=member).filter(interest=interest)
    category_slug = InterestCategory.objects.filter(interest=interest)[0].slug
    current_category = InterestCategory.objects.get(slug=category_slug)
    if is_already.count() == 0:
        interest_slug = tag
        new_interest = MemberInterest(slug=slug, interest=interest, member=member,
                                      category_slug=category_slug, interest_slug=interest_slug)
        new_interest.save()
        is_already = MemberInterestCategory.objects.filter(category=current_category).filter(member=member)
        # messages.success("Se añadió un interés al usuario.")
        if is_already.count() == 0:
            new_slug = generate_slug(MemberInterestCategory)
            new_category = MemberInterestCategory(slug=new_slug, category=current_category, member=member)
            new_category.save()
    return category_slug


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Skill.objects):
            return str(obj)
        return super().default(obj)
