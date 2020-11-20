import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['X-Token'] = getToken()
      config.headers['Authorization'] = 'JWT ' + getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const { data } = error.response

    if (typeof data === 'string') {
      Message({
        message: data,
        type: 'error',
        duration: 2 * 1000
      })
    } else {
      Object.keys(data).forEach(item => {
        Message({
          message: data[item],
          type: 'error',
          duration: 2 * 1000
        })
      })
    }

    console.log(error.response, 'interceptors')
    if (error.response.status === 401) {
      store.dispatch('user/logout')
    }
    return Promise.reject(error)
  }
)

export default service
