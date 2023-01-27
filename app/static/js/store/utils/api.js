import axios from 'axios';

class Api {
  constructor() {
    let service = axios.create({
      headers: {csrf: "", "Content-Type": "application/json"}
    });
    service.interceptors.response.use(this.handleSuccess, this.handleError);
    this.service = service;
  }

  setBaseUrl(url) {
    this.service.defaults.baseURL = url;
  }

  get(path, params) {
    return this.service.get(path, {params});
  }

  post(path, payload, token) {
    let contentType = "application/json"
    if (payload instanceof FormData) {
      contentType = "multipart/form-data"
    }

    return this.service.request({
      method: "POST",
      url: path,
      responseType: "json",
      data: payload,
      headers: {
        "X-CSRFToken": token,
        "Content-Type": contentType
      },
    });
  }

  put(path, payload, token) {
    let contentType = "application/json"
    if (payload instanceof FormData) {
      contentType = "multipart/form-data"
    }

    return this.service.request({
      method: 'PUT',
      url: path,
      responseType: 'json',
      data: payload,
      headers: {
        "X-CSRFToken": token,
        "Content-Type": contentType
      },
    });
  }

  delete(path, payload, token) {
    return this.service.request({
      method: 'DELETE',
      url: path,
      responseType: 'json',
      data: payload,
      headers: {'X-CSRFToken': token },
    });
  }

  getFake(response) {
    return new Promise((resolve, reject) => {
      setTimeout(
        resolve({
          data: response,
        }), Math.random() * 1000)
    })
  }
}

export default new Api;
