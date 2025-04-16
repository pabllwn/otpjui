@app.get("/")
async def root():
    return {"status": "Bot is alive!"}
