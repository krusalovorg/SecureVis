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
        const response = await fetch(URL_SERVER + "/account", {
            method: "GET",
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
    email: string;
    _id?: any;
    type: "admin" | "enterprise";
};

export type Enterprise = {
    name: string;
    email: string;
    type: "admin" | "enterprise";
    _id: string;
}

export const getEnterprises = async () => {
    try {
        const response = await fetch(URL_SERVER + "/enterprises", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as Enterprise[];
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};

export type Staff = {
    name: string;
    position: string;
    _id: string;
    statistics: any[];
}

export const getStaffs = async ({org_id}: {org_id: string}) => {
    try {
        const response = await fetch(URL_SERVER + "/staffs", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + getCookieToken(),
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data as Staff[];
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