import axios from 'axios';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const useFetchData = async (path: string): Promise<any> => {
  try {
    const config = useRuntimeConfig();
    const baseURL = config.public.baseURL as string;
    const { data } = await useFetch(path, {
      baseURL,
      method: 'GET',
      cache: 'force-cache',
    });
    return data.value;
  } catch (err) {
    console.log(err);
    console.log(err);
  }
};
export const useFetchData_2 = async (path: string): Promise<any> => {
  try {
    const config = useRuntimeConfig();
    const { data } = await useFetch(path, {
      method: 'GET',
      cache: 'force-cache',
    });
    return data.value;
  } catch (err) {
    console.log(err);
    console.log(err);
  }
};


export const useFetchData_MyAPI = async (path: string, params: any): Promise<any> => {
  try {
    const response = await axios.get(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': '',  // Nếu có token thì điền vào đây
      },
      params: params,  // Truyền params vào yêu cầu GET
    });

    return response.data;  
  } catch (err) {
    console.error('Error fetching data:', err);
    return null; 
  }
};


