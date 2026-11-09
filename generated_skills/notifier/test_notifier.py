"""Notifier Skill 測試（以 Spec 為基準）。"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, "/home/sam/代理人")

from notifier import Notifier


def test_send_sms():
    n = Notifier(["sms"])
    assert n.send("hi", "0912345678") is True


def test_send_email():
    n = Notifier(["email"])
    assert n.send("hi", "a@b.com") is True


def test_send_bulk():
    n = Notifier(["sms"])
    res = n.send_bulk(["m1", "m2"], ["p1", "p2"])
    assert res == [True, True]


def test_bulk_mismatch_raises():
    n = Notifier(["sms"])
    try:
        n.send_bulk(["m1"], ["p1", "p2"])
        assert False, "should raise"
    except ValueError:
        pass


# TODO: Repo branch untested
# 以下為 Repo 相容分支測試（註解）
# def test_legacy_sms():
#     from notifier import send_legacy_sms
#     assert send_legacy_sms(phone_number="0912", message="hi") is True