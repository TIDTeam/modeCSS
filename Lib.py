# -*- coding: utf-8 -*-
import sublime,os

def max_point(region):
    '''返回整理后的区间，(a,b)且a<b'''
    _a = region.a
    _b = region.b
    if _a >_b:
        return sublime.Region(_b,_a)
    else:
        return sublime.Region(_a,_b)

def expand_to_css_rule(view, cur_point):
    '''取得光标所在的样式定义'''
    rule = '^\w*[^{}\n]+ ?\{([^{}])*\}'
    css_rules = view.find_all(rule)
    for css_rule in css_rules:
        if css_rule.contains(cur_point):
            return css_rule
    # just return cur_point if not matching
    return cur_point

def build_time_suffix():
    '''生成时间缀'''
    import time
    t = time.time()
    t1 = time.localtime(time.time())
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())

def expand_to_style_in_html(view, cur_point):
    '''取得HTML文件中的样式定义'''
    rule = '<[\s]*?style[^>]*?>[\s\S]*?<[\s]*?\/[\s]*?style[\s]*?>'
    css_rules = view.find_all(rule)
    if css_rules:
        return css_rules
    return cur_point

def get_cur_point(view, region):
    '''取得当前行选区区间'''
    region = max_point(region)
    _x = sublime.Region(region.a, region.a) # 起点坐标
    _y = sublime.Region(region.b, region.b) # 终点坐标
    x = max_point(expand_to_css_rule(view, _x))
    y = max_point(expand_to_css_rule(view, _y))
    region = max_point(sublime.Region(x.a, y.b))
    return region

def expand_to_img_in_html(view, img_point):
    '''取得HTML文件中的img'''
    rule = '<img[^>]+src\s*=\s*[\'\"]([^\'\"]+)[\'\"][^>]*>'
    img_rules = view.find_all(rule)
    for img_rule in img_rules:
        if img_rule.contains(img_point):
            return img_rule
    return img_point

def get_dis(view):
    '''取得文件所在的目录'''
    if view.file_name():
        path = os.path.normpath(os.path.normcase(view.file_name()))
        return os.path.dirname(path)

def point_to_region(point_):
    '''转换成区域'''
    if len(point_) > 0:
        return sublime.Region(int(point_[0]), int(point_[1]))

def calc(path_a_,path_b_):
    ''' 路径转换
        path_a_：要转换的相对路径
        path_b_：绝对路径
    '''
    l = ["..",".",""]
    _path_a_ = path_a_
    _path_b_ = path_b_
    for v in path_a_:
        if v in l:
            if v == "..":
                _path_b_ = _path_b_[:-1]
                _path_a_ = _path_a_[1:]
            elif v == ".":
                _path_a_ = _path_a_[1:]
            elif v == "":
                return "\\".join(_path_b_)
        else:
            c = v.split(":")
            if len(c)>1:
                return "\\".join(_path_a_)
    return "\\".join(_path_b_) + "\\" + "\\".join(_path_a_)

def get_abs_path(path_a,path_b):
    '''将路径a的相对路径，转换为路径b的绝对路径'''
    if path_b:
        _path_b = os.path.normpath(os.path.normcase(path_b))
        if path_a:
            _path_a = os.path.normpath(os.path.normcase(path_a))
        else:
            _path_a = ""
        if os.path.isabs(_path_a):
            pass
        if not os.path.isabs(_path_b):
            pass
        _path_a_ = _path_a.split("\\")
        _path_b_ = _path_b.split("\\")
        return calc(_path_a_,_path_b_)

def region_and_str(region,region_,str_):
    '''转换区域为字符串'''
    r = []
    s = []
    l = []
    for _region in region_:
        _s = int(region.a) + int(_region.start())
        _e = int(region.a) + int(_region.end())
        r.append((_s,_e))
    for str in str_:
        s.append(str)
    for n in range(len(r)):
        l.append([r[n],s[n]])
    if l:
        return l