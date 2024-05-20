local function generate_id()
    local current_time = redis.call('TIME')[1]
    local id = current_time

    local existing_id = redis.call('GET', 'last_id')
    if existing_id then
        id = tonumber(existing_id) + 1
    end
    redis.call('SET', 'last_id', id)

    return id
end


-- Функция для создания новой сессии
local function createSession(expirationTime, userData)
    local sessionId = generate_id()
    local key = "session:" .. sessionId
    redis.call("HMSET", key, unpack(userData))
    if expirationTime then
        redis.call("EXPIRE", key, expirationTime)
    end
    return cjson.encode(key)
end

-- Функция для обновления данных в сессии или продления ее срока действия
local function updateSession(sessionId, expirationTime, newData)
    local key = "session:" .. sessionId
    redis.call("HMSET", key, unpack(newData))
    if expirationTime then
        redis.call("EXPIRE", key, expirationTime)
    end
    return cjson.encode(key)
end

-- Функция для завершения сессии
local function endSession(sessionId)
    local key = "session:" .. sessionId
    redis.call("DEL", key)
end

-- Функция для проверки активности сессии по ее идентификатору
local function checkSessionActivity(sessionId)
    local key = "session:" .. sessionId
    local sessionExists = redis.call("EXISTS", key)
    if sessionExists == 1 then
        local sessionData = redis.call("HGETALL", key)
        local result = {}
        for i=1, #sessionData, 2 do
            result[sessionData[i]] = sessionData[i+1]
        end
        local jsonString = cjson.encode(result)
        return jsonString
    else
        return cjson.encode("Session not found")
    end
end

-- Передача команды и аргументов в зависимости от запроса
local command = KEYS[1]
if command == "CREATE" then
    local lifeTime = KEYS[2]
    if #lifeTime == 0 then
        lifeTime = nil
    end
    return createSession(lifeTime, {unpack(KEYS, 3, #KEYS)})
elseif command == "UPDATE" then
    local lifeTime = KEYS[3]
    if #lifeTime == 0 then
        lifeTime = nil
    end
    return updateSession(KEYS[2], lifeTime, {unpack(KEYS, 4, #KEYS)})
elseif command == "END" then
    return endSession(KEYS[2])
elseif command == "CHECK" then
    return checkSessionActivity(KEYS[2])
else
    return KEYS
end
