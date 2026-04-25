/**
 * Abstract base class for communication providers.
 */
export class CommunicationProvider {
  /**
   * @param {string} module - Backend module
   * @param {string} action - Backend action
   * @param {any} params - Arguments
   * @returns {Promise<any>}
   */
  async call(module, action, params) {
    throw new Error('Method "call()" must be implemented.');
  }
}

export default CommunicationProvider;
