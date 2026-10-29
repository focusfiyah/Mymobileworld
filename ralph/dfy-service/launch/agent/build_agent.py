"""Create or update "Always Answered - Front Desk" on Ralph's ElevenLabs from ../AGENT.md (free: no call minutes).
Settings copied from Jean's tested line (jean-rameau diaspo-auto-school/agent): New York time zone, temperature 0,
eleven_v4_turbo, conference transfer to Ralph, end_call. Premade voice Sarah (not a clone; Jean's line uses Bella).
  python3 build_agent.py            # create (prints agent_id; save it in agent.json)
  python3 build_agent.py --update   # PATCH the agent in agent.json after AGENT.md changes
  python3 build_agent.py --assign PHONE_NUMBER_ID   # put the agent on the imported 516 number
"""
import json, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
MD = (HERE.parent / "AGENT.md").read_text()
CFG = HERE / "agent.json"
API = "https://api.elevenlabs.io/v1/convai"
VOICE = "EXAVITQu4vr4xnSDxMaL"            # Sarah, premade
TRANSFER = "+17864963177"                 # Ralph (AGENT.md, 2026-10-26)
SPOKEN_LINK = "calendly dot com, slash team R R G R P, slash thirty min"


def sec(h):
    return re.search(rf"## {h}[^\n]*\n(.*?)(?=\n## |\Z)", MD, re.S).group(1).strip()


def call(method, url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body is not None else None,
                                 {"Content-Type": "application/json"}, method=method)
    return json.loads(urllib.request.urlopen(req).read().decode() or "{}")


def body():
    prompt = sec("System prompt").replace("BOOKING_LINK_SPOKEN", SPOKEN_LINK)
    fields = {f: {"type": "string", "description": d} for f, d in {
        "caller_name": "caller's name", "business_name": "the caller's business, if they have one",
        "business_type": "what kind of business (plumber, salon...)", "caller_number": "caller ID number",
        "email": "email the caller gave, read back", "reason": "why they called",
        "sent_to_booking": "yes if pointed to the booking page, else no",
        "wanted_demo": "yes if they asked for the plumber demo, else no",
        "transferred": "yes if the call was transferred to Ralph, else no",
        "after_hours": "yes if Ralph was unavailable (outside 10am-6pm Mon-Sat New York), else no"}.items()}
    return {"name": "Always Answered - Front Desk",
            "conversation_config": {
                "agent": {"first_message": sec("First message").replace("\n", " "), "language": "en",
                          "prompt": {"prompt": prompt, "llm": "qwen35-397b-a17b", "temperature": 0.0, "timezone": "America/New_York",
                                     "built_in_tools": {
                                         "end_call": {"type": "system", "name": "end_call", "description": "",
                                                      "params": {"system_tool_type": "end_call"}},
                                         "transfer_to_number": {
                                             "type": "system", "name": "transfer_to_number",
                                             "description": "Transfer the caller to Ralph, only 10am-6pm Monday to Saturday New York time.",
                                             "params": {"system_tool_type": "transfer_to_number", "transfers": [{
                                                 "transfer_destination": {"type": "phone", "phone_number": TRANSFER},
                                                 "condition": "Ralph is AVAILABLE (Monday to Saturday, New York hour 10 to 17) AND the caller "
                                                              "asks for Ralph, the owner or a person, wants to sign up or talk price for "
                                                              "their business, asks something not covered, or sounds upset.",
                                                 "transfer_type": "conference"}]}}}}},
                "tts": {"voice_id": VOICE, "model_id": "eleven_v4_turbo"}},
            "platform_settings": {"data_collection": fields}}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        r = call("POST", f"{API}/agents/create", body())
        CFG.write_text(json.dumps({"agent_id": r["agent_id"]}, indent=1) + "\n"); print(r)
    elif a[0] == "--update":
        aid = json.loads(CFG.read_text())["agent_id"]; call("PATCH", f"{API}/agents/{aid}", body()); print("updated", aid)
    elif a[0] == "--assign":
        aid = json.loads(CFG.read_text())["agent_id"]
        print(call("PATCH", f"{API}/phone-numbers/{a[1]}", {"agent_id": aid}))
