declare global {
  interface Window {
    db: IDBDatabase;
  }
}

type HistoryComic = {
  id: string;
  title: string;
  thumbnail: string;
  authors: string | string[];
  status: string;
  reading_at: number;
  is_adult: boolean;
  last_reading: string;
  chapter_id: number;
};

export const initLocalDb = () => {
  const indexedDB = window.indexedDB;

  if (!indexedDB) return;

  const localDb = indexedDB.open('history', 1);

  localDb.onupgradeneeded = () => {
    const db = localDb.result;
    const store = db.createObjectStore('history', {
      keyPath: 'id',
      autoIncrement: false,
    });
    store.createIndex('reading_at', 'reading_at', { unique: true });
  };

  localDb.onsuccess = (e: any) => {
    window.db = e.target.result;
  };

  localDb.onerror = () => {
    console.error(localDb.error);
  };
};

export const historyAddComic = (data: HistoryComic) => {
  const db = window.db;
  const trans = db.transaction('history', 'readwrite');
  const store = trans.objectStore('history');
  store.put(data);
};

export const historyDeleteComic = (key: string) => {
  const db = window.db;
  const trans = db.transaction('history', 'readwrite');
  const store = trans.objectStore('history');
  store.delete(key);
};

// src/utils/localDB.ts

export const saveUserInfoToLocalStorage = (userInfo: any, expiryTimeInMinutes: number) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    const expiryTimestamp = new Date().getTime() + expiryTimeInMinutes * 60000; // Tính thời gian hết hạn
    const dataWithExpiry = {
      userInfo,
      expiry: expiryTimestamp,
    };
    localStorage.setItem('userInfo', JSON.stringify(dataWithExpiry));
  }
};

export const getUserInfoFromLocalStorage = () => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      const userInfo = localStorage.getItem('userInfo');
      // Kiểm tra nếu userInfo tồn tại và là chuỗi hợp lệ
      if (userInfo && userInfo !== 'undefined' && userInfo !== 'null') {
        try {
          const parsedData = JSON.parse(userInfo);
          const currentTime = new Date().getTime();

          // Kiểm tra nếu token đã hết hạn
          if (parsedData.expiry && currentTime < parsedData.expiry) {
            return parsedData.userInfo; // Token còn hợp lệ
          } else {
            localStorage.removeItem('userInfo'); // Xóa nếu token hết hạn
            return null;
          }
        } catch (error) {
          console.error('Error parsing user info from localStorage:', error);
          return null;  // Trả về null nếu JSON.parse gặp lỗi
        }
      } else {
        return null;  // Trả về null nếu không có dữ liệu hợp lệ
      }
    }
  } catch (error) {
    console.error('Error accessing localStorage:', error);
    return null;  // Trả về null nếu có lỗi khi truy cập localStorage
  }
};

export const clearUserInfoFromLocalStorage = () => {
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.removeItem('userInfo');
  }
};
