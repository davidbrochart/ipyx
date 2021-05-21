// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { XModel } from '..';

describe('X', () => {
  describe('XModel', () => {
    it('should be createable', () => {
      const model = createTestModel(XModel);
      expect(model).toBeInstanceOf(XModel);
      expect(model.get('_value')).toEqual('None');
    });

    it('should be createable with a value', () => {
      const state = { _value: 'Foo Bar!' };
      const model = createTestModel(XModel, state);
      expect(model).toBeInstanceOf(XModel);
      expect(model.get('_value')).toEqual('Foo Bar!');
    });
  });
});
