import axios from 'axios';

const MyAPI = axios.create({
  baseURL: 'http://localhost:8000/',
  headers: {
    'Content-Type': 'application/json',
  },
});

const OtruyenAPI = axios.create({
  baseURL: 'https://otruyenapi.com/v1/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// lưu danh sách truyện trang home
export const setHomeClient = async (comicId, switchStatus) => {
  try {
    const response = await MyAPI.post('/set_home_client', {
      id_comic: comicId,
      switch: switchStatus,
    });
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ MyAPI:", error);
    throw error;
  }
};

// Lấy danh sách home cho admnin
export const getHomeAdmin = async () => {
  try {
    const response = await MyAPI.get('/home_admin');
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// lấy danh sách home cho user
export const getHomeClient = async () => {
  try {
    const response = await MyAPI.get('/home_client');
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

export const getTruyenHome = async () => {
  try {
    const response = await OtruyenAPI.get('/home');
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// Hàm để lấy danh sách truyện
export const getDanhSach = async (type, page) => {
  try {
    const response = await OtruyenAPI.get(`/danh-sach/${type}`, {
      params: { page }
    });
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// Hàm để lấy các thể loại truyện
export const getTheLoai = async () => {
  try {
    const response = await OtruyenAPI.get('/the-loai');
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// Hàm để lấy danh sách truyện theo thể loại
export const getTruyenForTheLoai = async (slug, page) => {
  try {
    const response = await OtruyenAPI.get(`/the-loai${slug}`, {
      params: { page }
    });
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// Hàm tìm kiếm truyện
export const getSearch = async (keyword) => {
  try {
    const response = await OtruyenAPI.get('/tim-kiem', {
      params: { keyword },
    });
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

// lưu danh sách truyện trang home
export const setUserActive = async (userEmail, activateStatus) => {
  try {
    const response = await MyAPI.post('/set_user_active/', {
      email: userEmail,
      active: activateStatus,
    });
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ MyAPI:", error);
    throw error;
  }
};

// Lấy danh sách home cho admnin
export const getUsers = async () => {
  try {
    const response = await MyAPI.get('/table_users');
    return response.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu từ OtruyenAPI:", error);
    throw error;
  }
};

export default OtruyenAPI;
