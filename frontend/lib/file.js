import last from 'lodash/last'
import { v4 as uuidv4 } from 'uuid'

export function readImage(file) {
  const reader = new FileReader()
  reader.readAsDataURL(file)
  return new Promise((resolve, reject) => {
    reader.onload = () => {
      file.thumbnail = reader.result
      resolve(file)
    }
    reader.onerror = (error) => {
      reject(error)
    }
  })
}

export function randomFilename(file) {
  const extension = last(file.name.split('.'))
  return `${uuidv4()}.${extension}`
}
