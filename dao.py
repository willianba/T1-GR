import sqlite3


def get_limits_from_link():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM link")
    result = cursor.fetchall()
    conn.close()
    return result


def get_limits_from_ip():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM ip")
    result = cursor.fetchall()
    conn.close()
    return result


def get_limits_from_tcp():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM tcp")
    result = cursor.fetchall()
    conn.close()
    return result


def get_limits_from_udp():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM udp")
    result = cursor.fetchall()
    conn.close()
    return result


def get_limits_from_icmp():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM icmp")
    result = cursor.fetchall()
    conn.close()
    return result


def get_limits_from_snmp():
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT inferior, superior FROM snmp")
    result = cursor.fetchall()
    conn.close()
    return result


def update_limits_for_link(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE link
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()


def update_limits_for_ip(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ip
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()


def update_limits_for_tcp(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tcp
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()


def update_limits_for_udp(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE udp
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()


def update_limits_for_icmp(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE icmp
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()


def update_limits_for_snmp(limits):
    conn = sqlite3.connect("snmp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE snmp
        SET inferior = ?, superior = ?
        """, (limits["inferior"], limits["superior"]))
    conn.commit()
    conn.close()

