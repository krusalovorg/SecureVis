export const URL_SERVER = "http://127.0.0.1:5000";

async function requestData(url: string) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    return response.json();
}


export const getUserData = async (token: string) => {
    try {
        const response = await fetch(URL_SERVER + "/get_user_by_key", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as UserData;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};


export const getCookieToken = () => {
    let res = document.cookie.split("; ").find((row) => row.startsWith("access_token="))
    if (res) {
        res = res.replace("access_token=", "");
    }
    return res;
};
export const getImage = (image: string) => URL_SERVER + `/image/${image}`;

export type UserData = {
    name: string;
    surname: string;
    patronymic: string;
    phone_number?: string;
    email: string;
    birthday?: string;
    position?: string;
    isDoctor?: boolean;
    avatar: string,
    _id?: any;
    city?: string;
};

export const getDoctors = async (searchText: string) => {
    try {
        console.log('cookie:::', getCookieToken())
        const response = await fetch(URL_SERVER + "/show_doctor", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            },
            body: JSON.stringify({ search_item: searchText }),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as UserData[];
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};


export const getPositions = async () => {
    try {
        const response = await fetch(URL_SERVER + "/get_all_position", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            },
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as string[];
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};

export const getChats = async () => {
    try {
        console.log('cookie:::', getCookieToken())
        const response = await fetch(URL_SERVER + "/show_chats", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            }
        })
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as UserData[];
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};

export const getReferences = async () => {
    try {
        const response = await fetch(URL_SERVER + "/show_references", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as UserData[];
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};


export const logout = () => {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    document.location.reload();
}